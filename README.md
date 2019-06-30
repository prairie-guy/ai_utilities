# ai_utilities

A set of scripts useful with `fast.ai` lectures and libraries.

`image_download` is the primary function. It provides easy download of images from `google`, `bing` and/or `flickr` (though the later requires an `apikey`). It is intended for direct import of images within a python script or Jupyter Notebook. (This differs from previous versions intended for use as a CLI script.)

This is a new version based upon `icrawler` vs. `selenium`. It is much cleaner to install, use and extend. (It is an extension of work from https://github.com/cwerner/fastclass)

`make-train-valid` makes a train-valid directory and randomly copy files from labels_dir to sub-
directories. It is largely obsolete due to the new capabilities provided directly within `fastai`

## Installation
- `Anaconda` should be installed
- With `fastai` installed, the dependencies are: `icrawler` and `python-magic`
- `conda install -c hellock icrawler`
- `pip install python-magic`

## Example Usage
Download up to 500 images of each `class`, check each file to be a valid `jpeg` image, save to directory `dataset`, create imagenet-type directory structure and create `data = ImageDataBunch.from_folder(...)`
```
sys.path.append(your-parent-directory-of-ai_utilities)
from ai_utilities import *

path = Path.cwd()/'dataset'
pets = ['dog', 'cat', 'gold fish', 'tortise', 'snake' ]
for p in pets:
    image_download(p, 500)
    
make_train_valid('dataset')
data = ImageDataBunch.from_folder(path,ds_tfms=get_transforms(), size=224, bs=64).normalize(imagenet_stats)
```    

## Functions
### image_download.py
Downloads upto a number of images (typically limited to 1000) from a specified search engine, including `google`, `bing` and `flickr`. The `search_text` can be different from its `label`. Downloads are checked to be valid images. By default, images are saved to the directory `dataset`

```
usage: image_download(search_text:Path, num_images, label:str=None, engine:str='google', image_dir='dataset', apikey=None)
           where, 'engine'   = ['google'|'bing'|'all'|'flickr'],
                   'all'    = 'google' and 'bing',
                   'flickr' requires an apikey
           where, 'label' can be different from 'search_text'
```

### make_train_valid.py
From a directory containing sub-directories, each with a different class of images, make an imagenet-type directory structure.
It randomly copies files from `labels_dir` to sub-directories: `train`, `valid`, `test`. Creates an imagmenet-type directory usable by `ImageDataBunch.from_folder(dir,...)`

```
make_train_valid(labels_dir:Path, train:float=.8, valid:float=.2, test:float=0)
                           
positional arguments:
  labels_dir     Contains at least two directories of labels, each containing
                 files of that label

optional arguments:
  train=.8  files for training, default=.8
  valid=.2  files for validation, default=.2
  test=  0  files for training, default=.0
```

For example, given a directory:
```
catsdogs/
         ..cat/[*.jpg]
         ..dog/[*.jpg]
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
