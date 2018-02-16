#!/usr/bin/env python

###
# C. Bryan Daniels
# https://github.com/prairie-guy
# 2/7/2018
###

"""
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
"""



import os, sys, shutil, random, argparse
from pathlib import Path

parser = argparse.ArgumentParser(description = "Make a train-valid  directory  and randomly copy files from labels_dir to sub-directories")
parser.add_argument("labels_dir", help= "Contains at least two directories of labels, each containing files of that label")
parser.add_argument("--train", type=float, default=.8, help="files for training, default=.8")
parser.add_argument("--valid", type=float, default=.2, help="files for validation, default=.2")
parser.add_argument("--test", type=float, default=.0,  help="files for training,  default=.0")
args = parser.parse_args()

assert sum([args.train, args.valid, args.test]) == 1
assert Path(args.labels_dir).is_dir()
runs = {'train':args.train, 'valid':args.valid, 'test':args.test}
labels_path = Path(args.labels_dir)

for run in runs.keys():
    shutil.rmtree((labels_path / run), ignore_errors=True)

labels = [d.name for d in labels_path.iterdir() if d.is_dir()]
for label in labels:
    files = list((labels_path / label).iterdir())
    num_files = len(files)
    for run in runs.keys():
        os.makedirs(labels_path / run / label)
        take = round(num_files * runs[run])
        random.shuffle(files)
        for f in files[:take]:
            shutil.copy(f, (labels_path / run / label / f.name))
            print(f, (labels_path / run / label / f.name))
        files = files[take:]
        
     
