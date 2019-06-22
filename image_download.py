###
# C.Bryan Daniels
# 6/20/2019
# Adapted from github.com/atif93/google_image_downloader
# Adapted from github.com/cwerner/fastclass.git
###

# Install these modules before fastai to avoid clobbering pillow
# conda install -c hellock icrawler
# pip install python-magic

import os, sys, shutil
from pathlib import Path
import hashlib, magic
import icrawler
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler, BaiduImageCrawler, FlickrImageCrawler

__all__ = ['dedupe_images','filter_images','image_download']

def hashfile(path:Path)->str:
    """Create hash of file"""
    blocksize = 65536
    with open(path, 'rb') as f:
        hasher = hashlib.sha512()
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
    return hasher.hexdigest()

def dedupe_images(image_dir:Path)->int:
    """Delete duplicate images from image_dir """
    images = {}; dups = []
    path = Path(image_dir)
    for f in path.iterdir():
        h = hashfile(f)
        if h in images:
            images[h] = images[h] + 1
            dups.append(f)
        else:
            images[h] = 1
    n = len(dups)
    for f in dups:
        f.unlink()
    return n

def filter_images(image_dir:Path, img_type:str='JPEG')->int:
    """Filter (keep) only pictures of a specified type. The default is jpeg"""
    nons = 0
    path = Path(image_dir)
    for f in path.iterdir():
        jpeg = magic.from_file(f.as_posix())[:4]
        if f.is_file() and jpeg != img_type:
            nons = nons + 1
            f.unlink()
    return nons

def start_crawler(Crawler_class:icrawler, path:Path, search_text:str, num_images:int, file_idx_offset=0):
    """Kicks off a icarwler download."""
    crawler = Crawler_class(
            feeder_threads=2,
            parser_threads=2,
            downloader_threads=8,
            storage={'root_dir': path})
    crawler.crawl(keyword=search_text, max_num=num_images, file_idx_offset=file_idx_offset)
    
def start_flickr_crawler(path:Path, search_text:str, num_images:int, apikey:str):
    """Kicks off a Flickr download. Requires an apikey"""
    assert apikey != None, "Flickr requires an apikey: 'https://www.flickr.com/services/api/misc.api_keys.html'"
    crawler = FlickrImageCrawler(
            apikey,
            feeder_threads=2,
            parser_threads=2,
            downloader_threads=8,
            storage={'root_dir': path})
    crawler.crawl(tags=search_text, max_num=num_images, tag_mode='all')
    
def image_download(search_text:str, num_images:int, label:str=None, engine:str='google', image_dir='dataset', apikey=None):
    """
    Download images from google, bing or flickr
    usage: image_download(search_text:Path, num_images, label:str=None, engine:str='google', image_dir='dataset', apikey=None)
    where, engine   = ['google'|'bing'|'all'|'flickr'],
           'all'    = 'google' and 'bing',
           'flickr' requires an apikey,
    """
    assert engine=='google' or engine=='bing' or engine=='all' or 'flickr', "usage: -engine=['google'|'bing'|'all','flickr']"
    if label is None: label = search_text
    path = Path.cwd()/image_dir/label
    if Path.exists(path):
        response = input(f"'{label}' exists. Overwrite? [Y/n]: ")
        if response is 'Y':
            shutil.rmtree(path)
        else:
            print(f"'{label}' unchanged", end='\r')
            return
    if engine == 'google':
        start_crawler(GoogleImageCrawler, path, search_text, num_images)
    elif engine == 'bing':
        start_crawler(BingImageCrawler, path, search_text, num_images)
    elif engine == 'all':
        start_crawler(GoogleImageCrawler, path, search_text, num_images)
        start_crawler(BingImageCrawler, path, search_text, num_images, file_idx_offset='auto')
    elif engine == 'flickr':
        start_flickr_crawler(path, search_text, num_images, apikey)
    else:
        return "engine failure"
        
    nons = filter_images(path)   # Remove non-jpg images        
    dups = dedupe_images(path)   # Remove duplicates
    print()
    print("**********************************************************")
    print(f"Path:       {path}")
    print(f"Removed:    {dups} duplicate images")    
    print(f"Removed:    {nons} non-jpeg images ")
    print(f"Downloaded: {len(list(path.iterdir()))} images")
    print("**********************************************************")
