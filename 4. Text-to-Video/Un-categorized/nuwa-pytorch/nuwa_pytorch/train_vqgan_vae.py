from math import sqrt
import copy
from random import choice
from pathlib import Path
from shutil import rmtree

import torch
from torch import nn
import numpy as np

from PIL import Image
from torchvision.datasets import ImageFolder
import torchvision.transforms as T
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision.utils import make_grid, save_image

from einops import rearrange
from nuwa_pytorch.vqgan_vae import VQGanVAE
from nuwa_pytorch.optimizer import get_optimizer

# helpers

def exists(val):
    return val is not None

def noop(*args, **kwargs):
    pass

def cycle(dl):
    while True:
        for data in dl:
            yield data

def cast_tuple(t):
    return t if isinstance(t, (tuple, list)) else (t,)

def yes_or_no(question):
    answer = input(f'{question} (y/n) ')
    return answer.lower() in ('yes', 'y')

def accum_log(log, new_logs):
    for key, new_value in new_logs.items():
        old_value = log.get(key, 0.)
        log[key] = old_value + new_value
    return log

# classes

class MemmappedImageDataset(Dataset):
    def __init__(
        self,
        *,
        path,
        shape,
        random_rotate = True
    ):
        super().__init__()
        path = Path(path)
        assert path.exists(), f'path {path} must exist'
        self.memmap = np.memmap(str(path), mode = 'r', dtype = np.uint8, shape = shape)
        self.random_rotate = random_rotate

        image_size = shape[-1]
        self.transform = T.Compose([
            T.Resize(image_size),
            T.CenterCrop(image_size),
            T.ToTensor()
        ])

    def __len__(self):
        return self.memmap.shape[0]

    def __getitem__(self, index):
        arr = self.memmap[index]

        if arr.shape[0] == 1:
            arr = rearrange(arr, '1 ... -> ...')

        img = Image.fromarray(arr)
        img = self.transform(img)

        if self.random_rotate:
            img = T.functional.rotate(img, choice([0, 90, 180, 270]))
        return img

class ImageDataset(Dataset):
    def __init__(
        self,
        folder,
        image_size,
        exts = ['jpg', 'jpeg', 'png']
    ):
        super().__init__()
        self.folder = folder
        self.image_size = image_size
        self.paths = [p for ext in exts for p in Path(f'{folder}').glob(f'**/*.{ext}')]

        print(f'{len(self.paths)} training samples found at {folder}')

        self.transform = T.Compose([
            T.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
            T.Resize(image_size),
            T.RandomHorizontalFlip(),
            T.CenterCrop(image_size),
            T.ToTensor()
        ])

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, index):
        path = self.paths[index]
        img = Image.open(path)
        return self.transform(img)

# exponential moving average wrapper

class EMA(nn.Module):
    def __init__(
        self,
        model,
        beta = 0.99,
        ema_update_after_step = 1000,
        ema_update_every = 10,
    ):
        super().__init__()
        self.beta = beta
        self.online_model = model
        self.ema_model = copy.deepcopy(model)

        self.ema_update_after_step = ema_update_after_step # only start EMA after this step number, starting at 0
        self.ema_update_every = ema_update_every

        self.register_buffer('initted', torch.Tensor([False]))
        self.register_buffer('step', torch.tensor([0.]))

    def update(self):
        self.step += 1

        if self.step <= self.ema_update_after_step or (self.step % self.ema_update_every) != 0:
            return

        if not self.initted:
            self.ema_model.state_dict(self.online_model.state_dict())
            self.initted.data.copy_(torch.Tensor([True]))

        self.update_moving_average(self.ema_model, self.online_model)

    def update_moving_average(self, ma_model, current_model):
        def calculate_ema(beta, old, new):
            if not exists(old):
                return new
            return old * beta + (1 - beta) * new

        for current_params, ma_params in zip(current_model.parameters(), ma_model.parameters()):
            old_weight, up_weight = ma_params.data, current_params.data
            ma_params.data = calculate_ema(self.beta, old_weight, up_weight)

        for current_buffer, ma_buffer in zip(current_model.buffers(), ma_model.buffers()):
            new_buffer_value = calculate_ema(self.beta, ma_buffer, current_buffer)
            ma_buffer.copy_(new_buffer_value)

    def __call__(self, *args, **kwargs):
        return self.ema_model(*args, **kwargs)

# main trainer class

class VQGanVAETrainer(nn.Module):
    def __init__(
        self,
        vae,
        *,
        num_train_steps,
        lr,
        batch_size,
        grad_accum_every,
        wd = 0.,
        images_memmap_path = None,
        images_memmap_shape = None,
        folder = None,
        save_results_every = 100,
        save_model_every = 1000,
        results_folder = './results',
        valid_frac = 0.05,
        random_split_seed = 42,
        ema_beta = 0.995,
        ema_update_after_step = 2000,
        ema_update_every = 10,
        apply_grad_penalty_every = 4,
    ):
        super().__init__()
        assert isinstance(vae, VQGanVAE), 'vae must be instance of VQGanVAE'
        image_size = vae.image_size

        self.vae = vae
        self.ema_vae = EMA(vae, ema_update_after_step = ema_update_after_step, ema_update_every = ema_update_every)

        self.register_buffer('steps', torch.Tensor([0]))

        self.num_train_steps = num_train_steps
        self.batch_size = batch_size
        self.grad_accum_every = grad_accum_every

        all_parameters = set(vae.parameters())
        discr_parameters = set(vae.discr.parameters())
        vae_parameters = all_parameters - discr_parameters

        self.optim = get_optimizer(vae_parameters, lr = lr, wd = wd)
        self.discr_optim = get_optimizer(discr_parameters, lr = lr, wd = wd)

        # create dataset

        assert exists(folder) ^ exists(images_memmap_path), 'either folder or memmap path to images must be supplied'

        if exists(images_memmap_path):
            assert exists(images_memmap_shape), 'shape of memmapped images must be supplied'

        if exists(folder):
            self.ds = ImageDataset(folder, image_size = image_size)
        elif exists(images_memmap_path):
            self.ds = MemmappedImageDataset(path = images_memmap_path, shape = images_memmap_shape)

        # split for validation

        if valid_frac > 0:
            train_size = int((1 - valid_frac) * len(self.ds))
            valid_size = len(self.ds) - train_size
            self.ds, self.valid_ds = random_split(self.ds, [train_size, valid_size], generator = torch.Generator().manual_seed(random_split_seed))
            print(f'training with dataset of {len(self.ds)} samples and validating with randomly splitted {len(self.valid_ds)} samples')
        else:
            self.valid_ds = self.ds
            print(f'training with shared training and valid dataset of {len(self.ds)} samples')

        # dataloader

        self.dl = cycle(DataLoader(
            self.ds,
            batch_size = batch_size,
            shuffle = True
        ))

        self.valid_dl = cycle(DataLoader(
            self.valid_ds,
            batch_size = batch_size,
            shuffle = True
        ))

        self.save_model_every = save_model_every
        self.save_results_every = save_results_every

        self.apply_grad_penalty_every = apply_grad_penalty_every

        self.results_folder = Path(results_folder)

        if len([*self.results_folder.glob('**/*')]) > 0 and yes_or_no('do you want to clear previous experiment checkpoints and results?'):
            rmtree(str(self.results_folder))

        self.results_folder.mkdir(parents = True, exist_ok = True)

    def train_step(self):
        device = next(self.vae.parameters()).device
        steps = int(self.steps.item())
        apply_grad_penalty = not (steps % self.apply_grad_penalty_every)

        self.vae.train()

        # logs

        logs = {}

        # update vae (generator)

        for _ in range(self.grad_accum_every):
            img = next(self.dl)
            img = img.to(device)

            loss = self.vae(
                img,
                return_loss = True,
                apply_grad_penalty = apply_grad_penalty
            )

            accum_log(logs, {'loss': loss.item() / self.grad_accum_every})

            (loss / self.grad_accum_every).backward()

        self.optim.step()
        self.optim.zero_grad()


        # update discriminator

        if exists(self.vae.discr):
            discr_loss = 0
            for _ in range(self.grad_accum_every):
                img = next(self.dl)
                img = img.to(device)

                loss = self.vae(img, return_discr_loss = True)
                accum_log(logs, {'discr_loss': loss.item() / self.grad_accum_every})

                (loss / self.grad_accum_every).backward()

            self.discr_optim.step()
            self.discr_optim.zero_grad()

            # log

            print(f"{steps}: vae loss: {logs['loss']} - discr loss: {logs['discr_loss']}")

        # update exponential moving averaged generator

        self.ema_vae.update()

        # sample results every so often

        if not (steps % self.save_results_every):
            for model, filename in ((self.ema_vae.ema_model, f'{steps}.ema'), (self.vae, str(steps))):
                model.eval()

                imgs = next(self.dl)
                imgs = imgs.to(device)

                recons = model(imgs)
                nrows = int(sqrt(self.batch_size))

                imgs_and_recons = torch.stack((imgs, recons), dim = 0)
                imgs_and_recons = rearrange(imgs_and_recons, 'r b ... -> (b r) ...')

                imgs_and_recons = imgs_and_recons.detach().cpu().float().clamp(0., 1.)
                grid = make_grid(imgs_and_recons, nrow = 2, normalize = True, value_range = (0, 1))

                logs['reconstructions'] = grid

                save_image(grid, str(self.results_folder / f'{filename}.png'))

            print(f'{steps}: saving to {str(self.results_folder)}')

        # save model every so often

        if not (steps % self.save_model_every):
            state_dict = self.vae.state_dict()
            model_path = str(self.results_folder / f'vae.{steps}.pt')
            torch.save(state_dict, model_path)

            ema_state_dict = self.ema_vae.state_dict()
            model_path = str(self.results_folder / f'vae.{steps}.ema.pt')
            torch.save(ema_state_dict, model_path)

            print(f'{steps}: saving model to {str(self.results_folder)}')

        self.steps += 1
        return logs

    def train(self, log_fn = noop):
        device = next(self.vae.parameters()).device

        while self.steps < self.num_train_steps:
            logs = self.train_step()
            log_fn(logs)

        print('training complete')
