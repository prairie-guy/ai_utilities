# ai_utilities

A set of scripts useful with `fast.ai` lectures and libraries.

`image_download` is the primary function. It provides easy download of images from `bing`, `baidu`,  and/or `flickr` (though the later requires an `apikey`). It is intended for direct import of images within a python script or Jupyter Notebook. 


(Note: Previous versions supported google, however, icrawler has a bug using google, which I haven't had a chance to track down.)


`make-train-valid` makes a train-valid directory and randomly copy files from labels_dir to sub-
directories. It is largely obsolete due to the new capabilities provided directly within `fastai`

## Installation
-  The primary dependencies are: `icrawler` and `python-magic`
- `conda install -c hellock icrawler` or `pip install icrawler` (I've had recent trouble with the conda install)
- `pip install python-magic` or if it fails, try  `pip install python-magic-bin`

## Example Usage
Download up to 500 images of each `class`, check each file to be a valid `jpeg` image, save to directory `dataset`, create imagenet-type directory structure and create `data = ImageDataBunch.from_folder(...)`
```
sys.path.append(your-parent-directory-of-ai_utilities)
from ai_utilities import *

pets = ['dog', 'cat', 'gold fish', 'tortise', 'snake' ]
for p in pets:
    image_download(p, 500)
    
path = Path.cwd()/'dataset'    
make_train_valid(path)
data = ImageDataBunch.from_folder(path, ds_tfms=get_transforms(), size=224, bs=64).normalize(imagenet_stats)
```    

## Functions
### image_download.py
Downloads up to a number of images (typically limited to 1000) from a specified search engine, including `bing`, `baidu` and `flickr`. The `search_text` can be different from its `label`. Downloads are checked to be valid images. By default, images are saved to the directory `dataset`

```
usage: image_download(search_text:Path, num_images, label:str=None, engine:str='bing', image_dir='dataset', apikey=None)
           where, 'engine'   = ['bing'|'baidu'|'flickr'],
               'flickr' requires an apikey and
               'label' can be different from 'search_text'
```

### make_train_valid.py
From a directory containing sub-directories, each with a different class of images, make an imagenet-type directory structure.
It randomly copies files from `labels_dir` to sub-directories: `train`, `valid`, `test`. Creates an imagmenet-type directory usable by `ImageDataBunch.from_folder(dir,...)`

```
usage: make_train_valid(labels_dir:Path, train:float=.8, valid:float=.2, test:float=0)                           
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
