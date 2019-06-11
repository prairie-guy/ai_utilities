# ai_utilities

A set of scripts useful with `fast.ai` lectures and libraries.
The most common use case is downloading images for training vision models.

## Installation:
- `Anaconda`
- `Python >= 3`
- `git clone https://github.com/prairie-guy/ai_utilities.git `
- `conda install selenium`
- `cd ai_utilities`
- Download Geckodriver for your opearting system `https://github.com/mozilla/geckodriver/releases/` 
- `linux64` is shown below. (Adjust for win64 or macos)
- `wget https://github.com/mozilla/geckodriver/releases/geckodriver-v0.24.0-linux64.tar.gz`
- `tar xfvz geckodriver-v0.24.0-linux64.tar.gz`
- `mv geckodriver ~/bin/`, where `~/bin` in the the PATH


## Scripts
### image_download.py
Download of images (typically limited to 1000) from a specified search engine, currently `google` or `bing`. 

usage: image_download(searchtext:str, num_images:int, engine:str='google', gui:bool=False, timeout:float=0.3):
Select, search, download and save a specified number images using a choice of
search engines

positional arguments:
  searchtext            Search Image
  num_images            Number of Images

optional arguments:
  gui=False             Use Browser in the GUI
  engine='google'       Search engine {google|bing}
  timeout=0.3           Timeout for requests (May require optimization based upon connection)

Example:
sys.path.append(your-dir-parent-of-ai_utilities)
from ai_utilities import *
pets = ['dog', 'cat', 'gold fish', 'tortise', 'snake' ]
for p in pets:
    image_download(p, 500, timeout=.1)
    

### make_train_valid.py
From a directory containing sub-directories, each with a different class of images, make an imagenet-type directory structure.

`make_train_valid.py` creates a imagment-type directory usable by `ImageDataBunch.from_folder(dir,...)`
```
usage: make_train_valid(labels_dir:Path, train:float=.8, valid:float=.2, test:float=0) 
                           
Make a train-valid directory and randomly copy files from labels_dir to sub-
directories

positional arguments:
  labels_dir     Contains at least two directories of labels, each containing
                 files of that label

optional arguments:
  train=.8  files for training, default=.8
  valid=.2  files for validation, default=.2
  test=  0  files for training, default=.0

Example usage:
```

For example, given a directory:
```
catsdogs/
         ..cat/[*.jpg]
         ..dog/[*.jpg]
``` 
```
make_train_valid.py catsdogs --train .75 --valid .25
```
Creates the following directory structure:
```
catsdogs/
         ..cat/[*.jpg]
         ..dog/[*.jpg]
         ..train/
                 ..cat/[*.jpg]
                 ..dog/[*.jpg]
         ..valid/
                 ..cat/[*.jpg]
                 ..dog/[*.jpg]
```
