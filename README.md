## ai_utilities

Several useful scripts for use with `fast.ai` lectures and libraries.

`image_download` is the primary function. It provides easy download of images from `bing`, `google`, `baidu`,  and/or `flickr` (though the later requires an `apikey`). It is intended for direct import of images within a python script or Jupyter Notebook. 


`make-train-valid` makes a train-valid directory and randomly copy files from labels_dir to sub-
directories. It has largely been replaced by the capabilities within `fastai` but is still useful.

### Installation
- `pip install icrawler` 
- `pip install python-magic` or  `pip install python-magic-bin`
- `git clone https://github.com/prairie-guy/ai_utilities.git`


### image_download.py
Downloads up to a `n_images` (typically limited to 100-300) from a specified search engine, including `bing`, `baidu` and `flickr`. The `search_text` can be different from its `label`. Images are checked to be valid images and duplicates are eliminated. Images are saved to the directory `dataset` by defalult. (Based upon the excellent work of: https://github.com/hellock/icrawler)

```
usage: image_download(search_text:Path, n_images, label:str=None, engine:str='bing', image_dir='dataset', apikey=None)
           where, 'engine'   = ['bing'|'google'|baidu'|'flickr'],
                  'flickr' requires an apikey and
                  'label' can be different from 'search_text'
```

### Example Usage
Download up to 100 images of each `class`, check each file to be a valid `jpeg` image, save to directory `dataset` and create `data = ImageDataBunch.from_folder(...)`. Optionally create an imagenet-type directory structure.
```
import sys
sys.path.append('your-parent-directory-of-ai_utilities')
from ai_utilities import *
from pathlib import Path
from fastai.vision.all import *

for p in ['dog', 'goat', 'sheep']:
    image_download(p, 100)
path = Path.cwd()/'dataset'    
data = ImageDataLoaders.from_folder(path,valid_pct=0.2, item_tfms=Resize(224))

# Optionally, create an imagenet-type file directory.
make_train_valid(path)
data = ImageDataLoaders.from_folder(path, train='train', valid='valid', item_tfms=Resize(224))
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

