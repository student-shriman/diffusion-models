<img src="./make-a-video.png" width="400px"></img>

## Make-A-Video - Pytorch (wip)

Implementation of <a href="https://makeavideo.studio/">Make-A-Video</a>, new SOTA text to video generator from Meta AI, in Pytorch. They combine pseudo-3d convolutions (axial convolutions) and temporal attention and show much better temporal fusion.

The pseudo-3d convolutions isn't a new concept. It has been explored before in other contexts, say for protein contact prediction as <a href="https://www.biorxiv.org/content/10.1101/2022.08.04.502748v2.full">"dimensional hybrid residual networks"</a>.

The gist of the paper comes down to, take a SOTA text-to-image model (here they use DALL-E2, but the same learning points would easily apply to Imagen), make a few minor modifications for <a href="https://arxiv.org/abs/2204.03458">attention across time</a> and other ways to skimp on the compute cost, do frame interpolation correctly, get a great video model out.

<a href="https://www.youtube.com/watch?v=AcvmyqGgMh8">AI Coffee Break explanation</a>

## Appreciation

- <a href="https://stability.ai/">Stability.ai</a> for the generous sponsorship to work on cutting edge artificial intelligence research

- <a href="http://www.jonathanho.me/">Jonathan Ho</a> for bringing about a revolution in generative artificial intelligence through <a href="https://arxiv.org/abs/2006.11239">his seminal paper</a>

- <a href="https://github.com/arogozhnikov">Alex</a> for <a href="https://github.com/arogozhnikov/einops">einops</a>, an abstraction that is simply genius. No other word for it.

## Install

```bash
$ pip install make-a-video-pytorch
```

## Usage

Passing in video features

```python
import torch
from make_a_video_pytorch import Pseudo3DConv, SpatioTemporalAttention

conv = Pseudo3DConv(
    dim = 256,
    kernel_size = 3
)

attn = SpatioTemporalAttention(
    dim = 256,
    dim_head = 64,
    heads = 8
)

video = torch.randn(1, 256, 8, 16, 16) # (batch, features, frames, height, width)

conv_out = conv(video) # (1, 256, 8, 16, 16)
attn_out = attn(video) # (1, 256, 8, 16, 16)
```

Passing in images (if one were to pretrain on images first), both temporal convolution and attention will be automatically skipped. In other words, you can use this straightforwardly in your 2d Unet and then port it over to a 3d Unet once that phase of the training is done. The temporal modules are initialized to output identity as the paper had done.

```python
import torch
from make_a_video_pytorch import Pseudo3DConv, SpatioTemporalAttention

conv = Pseudo3DConv(
    dim = 256,
    kernel_size = 3
)

attn = SpatioTemporalAttention(
    dim = 256,
    dim_head = 64,
    heads = 8
)

images = torch.randn(1, 256, 16, 16) # (batch, features, height, width)

conv_out = conv(images) # (1, 256, 16, 16)
attn_out = attn(images) # (1, 256, 16, 16)
```

You can also control the two modules so that when fed 3-dimensional features, it only does training spatially

```python
import torch
from make_a_video_pytorch import Pseudo3DConv, SpatioTemporalAttention

conv = Pseudo3DConv(
    dim = 256,
    kernel_size = 3
)

attn = SpatioTemporalAttention(
    dim = 256,
    dim_head = 64,
    heads = 8
)

video = torch.randn(1, 256, 8, 16, 16) # (batch, features, frames, height, width)

# below it will not train across time

conv_out = conv(video, convolve_across_time = False) # (1, 256, 8, 16, 16)
attn_out = attn(video, attend_across_time = False) # (1, 256, 8, 16, 16)
```

## Todo

- [ ] wire up <a href="https://github.com/lucidrains/dalle2-pytorch">dalle2-pytorch</a> unet with pseudo 3d convs + spatial temporal attention
- [ ] give attention the best positional embeddings research has to offer
- [ ] soup up the attention
- [ ] offer a function, similar to how MosaicML's approach, that automatically rigs a 2d-unet from dalle2-pytorch to be 3d
- [ ] consider learned exponential moving average across time from https://github.com/lucidrains/Mega-pytorch

## Citations

```bibtex
@misc{Singer2022,
    author  = {Uriel Singer},
    url     = {https://makeavideo.studio/Make-A-Video.pdf}
}
```

```bibtex
@inproceedings{rogozhnikov2022einops,
    title   = {Einops: Clear and Reliable Tensor Manipulations with Einstein-like Notation},
    author  = {Alex Rogozhnikov},
    booktitle = {International Conference on Learning Representations},
    year    = {2022},
    url     = {https://openreview.net/forum?id=oapKSVM2bcj}
}
```
