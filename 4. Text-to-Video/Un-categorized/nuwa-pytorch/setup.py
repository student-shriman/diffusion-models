from setuptools import setup, find_packages

setup(
  name = 'nuwa-pytorch',
  packages = find_packages(exclude=[]),
  include_package_data = True,
  version = '0.7.7',
  license='MIT',
  description = 'NÜWA - Pytorch',
  long_description_content_type = 'text/markdown',
  author = 'Phil Wang',
  author_email = 'lucidrains@gmail.com',
  url = 'https://github.com/lucidrains/nuwa-pytorch',
  keywords = [
    'artificial intelligence',
    'attention mechanism',
    'transformers'
  ],
  install_requires=[
    'einops>=0.4.1',
    'ftfy',
    'pillow',
    'regex',
    'torch>=1.6',
    'torchvision',
    'tqdm',
    'unfoldNd',
    'vector-quantize-pytorch>=0.4.10'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
  ],
)
