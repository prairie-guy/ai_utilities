# ai_utilities

A set of scripts useful with `fast.ai` lectures and libraries.
The most common use case is downloading images for training vision models.

## image_download.py
Command-line download of images (typically limited to 1000) from a specified search engine.

`image_download.py` is useful in several respects:
- Operates in `headless-mode`. Can be used without access to a gui browser.
- Operates from the `command-line`.
- `Scriptable`. (Easily write a bash script to download 10 classes of images.)
- Downloads images directly to GPU server. (No need to transfer images from local computer to gpu-server.)
- Specify search enginge. (Currently 'google' or 'bing')
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

Installation:
- `Python >= 3`
- `conda install selenium`
- `cd ai_utilities`
- Download Geckodriver for your opearting system `https://github.com/mozilla/geckodriver/releases/` (For example: Ubuntu)
- `wget https://github.com/mozilla/geckodriver/releases/geckodriver-v0.24.0-linux64.tar.gz`
- `tar xfvz geckodriver-v0.24.0-linux64.tar.gz`
- `mv geckodriver ~/bin/`, where `~/bin` is a dir in PATH

Usage:
image_download.py dog 200 (Download 200 dog images using default google engine)
image_download.py cat 500 --engine bing (Download using bing engine)
image_download.py dog 200  --gui (Download with browser showing in GUI)


## filter_img.sh
Use `file` to determine the type of picture then filter (keep) only pictures of a specified type.
Different image formats may break training algorithims.

Images are filtered in place, i.e., non-JPEG files are deleted. (This can be modified within the script.)
```
Usage: filter_img.sh image_directory
```

Example:`filter_image.sh dogs/`

## Sample work flow: Download images of two classes of cars and remove non-jpeg images
```
image_download.py 'bmw' 500
image_download.py 'cadillac' 500
mv dataset cars
filter_img.sh cars/bmw
filter_img.sh cars/cadillac
```

## make_train_valid.py
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

## ai_utils.py

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
