#!/usr/bin/env python

###
# C. Bryan Daniels
# https://github.com/prairie-guy
# 2/7/2018
###

import os, sys, shutil, random, argparse
from pathlib import Path

__all__ = ['make_train_valid']

def make_train_valid(labels_dir:Path, train:float=.8, valid:float=.2, test:float=0):
    """
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
"""
    assert sum([train, valid, test]) == 1
    assert (Path(labels_dir).is_dir())
    labels_path = Path(labels_dir)
    runs = {'train':train, 'valid':valid, 'test':test}
    

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
                #print(f, (labels_path / run / label / f.name))
            files = files[take:]
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Make a train-valid  directory  and randomly copy files from labels_dir to sub-directories")
    parser.add_argument("labels_dir", help= "Contains at least two directories of labels, each containing files of that label")
    parser.add_argument("--train", type=float, default=.8, help="files for training, default=.8")
    parser.add_argument("--valid", type=float, default=.2, help="files for validation, default=.2")
    parser.add_argument("--test", type=float, default=.0,  help="files for testing,  default=.0")
    args = parser.parse_args()
     
    make_train_valid(args.labels_dir, args.train, args.valid, args.test)
    
