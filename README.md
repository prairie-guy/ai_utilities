# ai_utilities

A set of scripts useful in deep learning and AI purposes, originally for use with `fast.ai` lectures and libraries.

## image_download.py
Download any number of images from Google image search. image_download.py is useful in several respects:
- Because is utilizes selenium, it is not limitied by google api limit on the number of downloaded images.
- It can operate in `headless` mode, which means it can be used on a server without access to a gui browser.
- In addtionto Firefox, the script can be modified to use other browsers such as Chrome.

Usage:
`python image-download.py query num_images`

Example:`python image-download.py 'dog' 200`

Note: geckodriver is used for Firefox and needs to be installed in PATH, or else modify the script to use a sepcified location.

## filter-img.sh
Use 'file' to determine the type of picture then filter (keep) only pictures of a specified type.

Images are filtered in place, i.e., non-JPEG files are deleted. (This can be modified within the script.)

Usage:  `filter-img image_directory`
Example:`filter-image pictures`

## make-train-valid.sh
Set up `valid` and `train` directories for use in deep learning models.

Usage:   `make-train-valid.sh dir_containing_labels number_of_valid`
- dir_containing_labels contains subdirectories lable1, label2...,  each containing files of the corresponding label.
- number_of_valids is the number of validations to use for each label

Example: `make-train-valid.sh catsdogs 100`

These should be used for educational purposes only. Copyright is owned by the respective websites.
