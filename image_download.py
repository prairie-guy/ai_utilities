#!/usr/bin/env python

###
# C.Bryan Daniels
# 2/8/2018
# Very minor tweaks to:  github.com/atif93/google_image_downloader
###

import os, sys, time
import json, requests, shutil
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options


# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"

# Usage: python image_download.py 'searchtext' 'num_requested'

def main():
        ### Local:
        # driver = webdriver.Firefox()

        ## HEADLESS: set to work with headless Firefox, assumes  geckodriver is in the searchpath or is specified in executable_path, below
	options = Options()
	options.add_argument('-headless')
	driver = Firefox(executable_path='geckodriver', firefox_options=options)
        ##

	searchtext = sys.argv[1]
	num_requested = int(sys.argv[2])
	number_of_scrolls = num_requested / 400 + 1
	# number_of_scrolls * 400 images will be opened in the browser

	if not os.path.exists(download_path + searchtext.replace(" ", "_")):
		os.makedirs(download_path + searchtext.replace(" ", "_"))

	url = f'https://www.google.co.in/search?q={searchtext}&source=lnms&tbm=isch'


	driver.get(url)

	headers = {}
	headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
	extensions = { "jpg", "jpeg", "png", "gif" }
	img_count = 0
	downloaded_img_count = 0

	for _ in range(int(number_of_scrolls)):
		for __ in range(10):
			# multiple scrolls needed to show all 400 images
			driver.execute_script("window.scrollBy(0, 1000000)")
			time.sleep(0.2)
		# to load next 400 images
		time.sleep(0.5)

		try:
			driver.find_element_by_xpath("//input[@value='Show more results']").click()

		except Exception as e:
			print (f'Less images found: {e}')
			break

	imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
	print ("Total images:", len(imges), "\n")

	for img in imges:

		img_count += 1
		img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
		img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
		print (f'Downloading image {img_count} : {img_url}')

		try:
			if img_type not in extensions: img_type = "jpg"

			r = requests.get(img_url, stream=True, headers=headers)
			if r.status_code == 200:
				with open(download_path + searchtext.replace(" ", "_") + "/" + str(downloaded_img_count) + "." + img_type, "wb") as f:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)
					downloaded_img_count += 1

		except Exception as e:
			print (f'Download failed: {e}')

		finally:
			print('')

		if downloaded_img_count >= num_requested:
			break

	print (f'Total downloaded: {downloaded_img_count}/{img_count}')
	driver.quit()

if __name__ == "__main__":
	main()
