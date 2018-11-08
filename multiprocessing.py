#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 21:48:26 2018

@author: guru
"""

from multiprocessing import Pool
import time
from urllib.request import urlopen

def millis():
  return int(round(time.time() * 1000))

def http_get(url):
  start_time = millis()
  result = {"url": url, "data": urlopen(url, timeout=5).read()[:100]}
  print(url + " took " + str(millis() - start_time) + " ms")
  return result
  
urls = ['http://www.google.com/', 'https://foursquare.com/', 'http://www.yahoo.com/', 'http://www.bing.com/', "https://www.yelp.com/"]

pool = Pool(processes=2)

start_time = millis()
results = pool.map(http_get, urls)

print("\nTotal took " + str(millis() - start_time) + " ms\n")

for result in results:
  print(result)