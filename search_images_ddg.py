#!/usr/bin/env python

### search_images_ddg.py
### C. Bryan Daniels
### 9/1/2020
### Adopted from https://github.com/deepanprabhu/duckduckgo-images-api
###

import requests, re, json, time, sys, os
from pathlib import Path

__all__ = ['search_images_ddg']

def search_images_ddg(keywords,max_n=100):
    """Search for 'keywords' with DuckDuckGo and return a unique urls of 'max_n' images"""
    url        = 'https://duckduckgo.com/'
    params     = {'q':keywords}
    res        = requests.post(url,data=params)
    searchObj  = re.search(r'vqd=([\d-]+)\&',res.text)
    if not searchObj: print('Token Parsing Failed !'); return
    requestUrl = url + 'i.js'
    headers    = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    params     = (('l','us-en'),('o','json'),('q',keywords),('vqd',searchObj.group(1)),('f',',,,'),('p','1'),('v7exp','a'))
    urls       = []
    while True:
        try:
            res  = requests.get(requestUrl,headers=headers,params=params)
            data = json.loads(res.text)
            for obj in data['results']:
                urls.append(obj['image'])
                max_n = max_n - 1
                if max_n < 1: return list(set(urls))
            if 'next' not in data: return list(set(urls))
            requestUrl = url + data['next']
        except:
            pass

if __name__ == "__main__":
    def print_urls(urls):
        for url in urls:
            print(url)
    if len(sys.argv)    == 2: print_urls(search_images_ddg(sys.argv[1])) 
    elif len(sys.argv)  == 3: print_urls(search_images_ddg(sys.argv[1],int(sys.argv[2]))) 
    else: print("usage: search(keywords,max_n=100)")
