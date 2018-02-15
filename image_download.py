#!/usr/bin/env python

###
# C.Bryan Daniels
# 2/14/2018
# Adapted from github.com/atif93/google_image_downloader
###

# Usage: python image_download.py 'searchtext' 'num_images' [--gui]

import sys, time, json, requests, shutil
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

args = sys.argv
searchtext = args[1]
label = searchtext.replace(" ", "_")
num_images = int(args[2])

############################################################################################
# Customized by search engine
def get_urls_bing(driver, searchtext):
    request = f'https://www.bing.com/images/search?q={searchtext}'
    driver.get(request)
    # Find Button: "See More Images"
    for i in range(10):
        driver.execute_script(f'window.scrollBy(0, 1000)')
        time.sleep(.2)
        try:
            driver.find_element_by_xpath("//a[@class='btn_seemore']").click()
            print("Found: See More Images->", i)
            break
        except:
            None
    # Scroll through end of the document
    for i in range(40):
        driver.execute_script("window.scrollBy(0, 1000)")
        print("Scrolling-> ", i)
        time.sleep(.2)
    # Get urls of images
    def make_url(xpath): return json.loads(xpath.get_attribute('m'))['murl']
    xpaths = driver.find_elements_by_xpath('//a[@class="iusc"]')
    return [make_url(xpath) for xpath in xpaths]

def get_urls_google(driver, searchtext):
    scrolls = 1 + int(num_images / 400)
    request = f'https://www.google.co.in/search?q={searchtext}&source=lnms&tbm=isch'
    driver.get(request)
    # Find Button: "See More Images"
    for i in range(5):
        for j in range(10):
            driver.execute_script("window.scrollBy(0, 10000)")
            time.sleep(0.2)
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//input[@value='Show more results']").click()
            print("Found: See More Images->",i)
        except Exception as e:
            break
    # Get urls
    def make_url(xpath): return json.loads(xpath.get_attribute('innerHTML'))['ou']
    xpaths = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    return [make_url(xpath) for xpath in xpaths]

############################################################################################
def make_driver():
    if len(args)== 4 and args[3] == '--gui':
        driver = webdriver.Firefox()
    else:
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='geckodriver', firefox_options=options)
    return driver

def check_suffix(path):
    if path.suffix not in [ ".jpg", ".jpeg", ".png", ".gif"]:
        return path.with_suffix(".jpg")
    else:
        return path

def get_and_save_images(urls, label):
    headers = {'User-Agent' :  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"}
    # Make label_dir
    label_dir = Path('dataset')  / label
    if not Path.exists(label_dir / label):
        label_dir.mkdir(parents=True,exist_ok=True)
    # Get images and save to label_dir
    num_downloaded = 0
    for (i, image) in enumerate(urls, 1):
        try:
            req = requests.get(image, stream=True, headers=headers)
            if req.status_code == 200:
                with open(check_suffix(label_dir / str(num_downloaded)), "wb") as fname:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, fname)
                    num_downloaded += 1
                    print (f'Image {i} : {image}')
        except Exception as e:
            print (f'Download failed: {e}')
        finally:
            None
        if num_downloaded >= num_images:
            break
    print(f'Downloaded {num_downloaded}/{num_images}')

## __Main Script__    
driver = make_driver()
#urls = get_urls_bing(driver,searchtext)
urls = get_urls_google(driver,searchtext)
print (f'Found {len(urls)} images')
get_and_save_images(urls, label)
driver.quit()


