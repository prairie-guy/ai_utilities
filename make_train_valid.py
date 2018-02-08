#!/usr/bin/env python

###
# C. Bryan Daniels
# https://github.com/prairie-guy
# 2/7/2018
###

### Change if needed:
runs  = {'train':.8, 'valid':.2}
# runs  = {'train':.75, 'valid':.2, 'test':.05} 
###

assert sum(runs.values()) == 1

import os, sys, shutil, random
from pathlib import Path

args = sys.argv
script_name = args[0]
if len(args) != 2  or not Path(args[1]).is_dir():
    print(f"usage: {script_name} labels_dir")
    sys.exit()
labels_path = Path(args[1])

for run in runs.keys():
    shutil.rmtree((labels_path / run), ignore_errors=True)
        
labels = [d.name for d in labels_path.iterdir() if d.is_dir()]
if len(labels) < 2:
    print(f"usage: {script_name} labels_dir, containing at 2 least directories each named as a label and containing files of that label")
    sys.exit()

for label in labels:
    files = list((labels_path / label).iterdir())
    num_files = len(files)
    for run in runs.keys():
        os.makedirs(labels_path / run / label)
        take = round(num_files * runs[run])
        random.shuffle(files)
        for f in files[:take]:
            shutil.copy(f, (labels_path / run / label / f.name))
            #os.symlink(f, (labels_path / run / label / f.name))
            print(f, (labels_path / run / label / f.name))
        files = files[take:]
        
     
