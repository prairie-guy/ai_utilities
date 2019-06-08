# ai_utilities

A set of scripts useful with `fast.ai` lectures and libraries.
The most common use case is downloading images for training vision models.

## Installation:
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
Command-line download of images (typically limited to 1000) from a specified search engine.

`image_download.py` is useful in several respects:
- Operates in `headless-mode`. (Can be used without access to a gui browser.)
- Operates from the `command-line`.
- `Scriptable`. (Easily write a bash script to download 10 classes of images.)
- Downloads images directly to GPU server. (No need to transfer images from local computer to gpu-server.)
- Specify search enginge. (Currently `google` or `bing`)
- Default browser is Firefox. (The script can be modified to use other browsers such as Chrome.)
- Optionally, operates in `GUI-mode`. (Good for debugging.)
```
usage: image_download.py [-h] [--gui] [--engine {google,bing}]
                         searchtext num_images

Select, search, download and save a specified number images using a choice of
search engines

positional arguments:
  searchtext            Search Image
  num_images            Number of Images

optional arguments:
  -h, --help            show this help message and exit
  --gui, -g             Use Browser in the GUI
  --engine {google,bing}, -e {google,bing}
                        Search Engine, default=google
```

Examples:
- `image_download.py dog 200` (Download 200 dog images using default google engine)
- `image_download.py cat 500 --engine bing` (Download using bing engine)
- `image_download.py dog 200`  --gui (Download with browser showing in GUI)


### filter_img.sh
Filter (keep) only pictures of a specified type. The default is JPEG
Differences in image formats will break training algorithims.

Images are filtered in place, i.e., non-JPEG files are deleted. (This can be modified within the script.)
```
Usage: filter_img.sh image_directory
```

Example:`filter_image.sh dogs/`

### make_train_valid.py
From a directory containing sub-directories, each with a different class of images, make an imagenet-type directory structure.

`make_train_valid.py` creates a imagment-type directory usable by `ImageDataBunch.from_folder(dir,...)`
```
usage: make_train_valid.py [-h] [--train TRAIN] [--valid VALID] [--test TEST]
                           labels_dir

Make a train-valid directory and randomly copy files from labels_dir to sub-
directories

positional arguments:
  labels_dir     Contains at least two directories of labels, each containing
                 files of that label

optional arguments:
  -h, --help     show this help message and exit
  --train TRAIN  files for training, default=.8
  --valid VALID  files for validation, default=.2
  --test TEST    files for training, default=.0
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

## Sample work flows: 

#### Bash script to download images of two classes of cars, remove non-jpeg images and make imagenet-type file structure.
```
image_download.py 'bmw' 500
image_download.py 'cadillac' 500
mv dataset cars
filter_img.sh cars/bmw
filter_img.sh cars/cadillac
make_train_valid.py cars
```

#### Jupyter version of script
```
from fastai.vision import *
birds = ['crow','robin','raven','parrot','sparrow']
for b in birds:
    !~/ai_utilities/image_download.py $b 100
    !~/ai_utilities/filter_img.sh dataset/$b
!~/ai_utilities/make_train_valid.py dataset/
path = Path.cwd()/'dataset'
data = ImageDataBunch.from_folder(path,ds_tfms=get_transforms(), size=224, bs=64).normalize(imagenet_stats)
```

## Misc ai_utils.py scripts

```
ai_utils.py
contains:
atttributes_of(obj, *exclude): -> prints obj attributes
methods_of(obj,lr=False):      -> prints obj methods

usage: import ai_utils

> data = ImageClassifierData.from_paths(PATH, tfms=tfms_from_model(arch, sz))
> attributes_of(data.trn_dl.dataset,'fnames')
c: 2
fnames: ...
is_multi: False
is_reg: False
n: 23000
path: data/dogscats/
sz: 224
y: [0 0 0 ... 1 1 1]

> methods_of(data.trn_dl.dataset)
denorm(arr):
get(tfm, x, y):
get_c():
get_n():
get_sz():
get_x(i):
get_y(i):
resize_imgs(targ, new_path):
transform(im, y=None):
```
