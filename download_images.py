#!/usr/bin/env python

### download_images.py
### C. Bryan Daniels
### 9/1/2020
### Adopted from https://github.com/deepanprabhu/duckduckgo-images-api
###

import requests, re, sys, os, requests, threading
from pathlib import Path
from fastprogress import progress_bar
from threading import Thread

__all__ = ['download_images']

def download_images(urls=None, url_file=None, dest='dataset',max_pics=1000, timeout=5):  
    "Download images listed in text file `url_file` to path `dest`, at most `max_pics`"
    if urls is None: urls = (open(url_file)).read().strip().split("\n")[:max_pics]
    dest = Path(dest)
    dest.mkdir(exist_ok=True)
    download_image_inner(dest, list(enumerate(urls)), timeout=timeout)
    
def download_image_inner(dest, inp, timeout=5):
    for (i,url)  in inp:
        suffix = re.findall(r'\.\w+?(?=(?:\?|$))', url)
        suffix = suffix[0] if len(suffix)>0  else '.jpg'
        try:
            Thread(target=download_url,
                             args = (url, dest/f"{i:08d}{suffix}"),
                             kwargs = {'overwrite':True, 'show_progress':False, 'timeout':timeout}).start()
            #download_url(url, dest/f"{i:08d}{suffix}", overwrite=True, show_progress=False, timeout=timeout)
        except Exception as e: f"Couldn't download {url}."

def download_url(url, dest, overwrite=False, pbar=None, show_progress=True, chunk_size=1025*1024,
                 timeout=5, retries=5):
    "Download `url` to `dest` unless it exists and not `overwrite`"
    if os.path.exists(dest) and not overwrite: return

    s = requests.Session()
    s.mount('http://',requests.adapters.HTTPAdapter(max_retries=retries))
    # additional line to identify as a firefox browser, see fastai/#2438
    s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'})
    u = s.get(url, stream=True, timeout=timeout)
    try: file_size = int(u.headers["Content-Length"])
    except: show_progress = False

    with open(dest, 'wb') as f:
        nbytes = 0
        if show_progress: pbar = progress_bar(range(file_size), leave=False, parent=pbar)
        try:
            if show_progress: pbar.update(0)
            for chunk in u.iter_content(chunk_size=chunk_size):
                nbytes += len(chunk)
                if show_progress: pbar.update(nbytes)
                f.write(chunk)
        except requests.exceptions.ConnectionError as e:
            fname = url.split('/')[-1]
            data_dir = dest.parent
            print(f'\n Download of {url} has failed after {retries} retries\n'
                  f' Fix the download manually:\n'
                  f'$ mkdir -p {data_dir}\n'
                  f'$ cd {data_dir}\n'
                  f'$ wget -c {url}\n'
                  f'$ tar xf {fname}\n'
                  f' And re-run your code once the download is successful\n')

if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        download_images(url_file=args[0])
    except:
        print("usage: download_images(urls=None, url_file=None,  dest='dataset',max_pics=1000, timeout=4):")
    # if len(sys.argv)    == 2: print_urls(search_images_ddg(sys.argv[1]))
    # elif len(sys.argv)  == 3: print_urls(search_images_ddg(sys.argv[1],int(sys.argv[2])))
    # else: print("usage: search(keywords,max_n=100)")
