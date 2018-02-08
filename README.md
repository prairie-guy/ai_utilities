# ai_utilities

A set of scripts useful in deep learning and AI purposes, originally for use with `fast.ai` lectures and libraries.

## make_train_valid.py
Set up `train` and `valid` directories for use in deep learning models.

Usage:   `make_train_valid.py dir_containing_labels`
- dir_containing_labels contains sub-directories lable1, label2...,  each containing files of the corresponding label.
- Default settings for `train` and `valid` are `.80` and `.20`, respectively. These can be modified in the script.
- In addition to `train` and `valid`, `test` can be added. Edit script: `runs  = {'train':.75, 'valid':.2, 'test':.05}`

Example: `make_train_valid.py catsdogs`

## image_download.py
Download any number of images from Google image search. image_download.py is useful in several respects:
- Because is utilizes selenium, it is not limited by google api limit on the number of downloaded images.
- It can operate in `headless` mode, which means it can be used on a server without access to a gui browser.
- The default browser is Firefox. The script can be modified to use other browsers such as Chrome.

Usage:   `image_download.py query num_images`

Example: `image_download.py 'dog' 200`

Note: geckodriver is used for Firefox and needs to be installed in PATH, or else modify the script to use a specified location.

## filter_img.sh
Use `file` to determine the type of picture then filter (keep) only pictures of a specified type.

Images are filtered in place, i.e., non-JPEG files are deleted. (This can be modified within the script.)

Usage:  `filter_img image_directory`
Example:`filter_image pictures`

These should be used for educational purposes only. Copyright is owned by the respective websites.
