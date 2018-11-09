#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:40:50 2018

@author: guru
"""

from multiprocessing import Pool
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

url = "http://tamilrockers.ph"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")

firstpost = soup.find(class_="ipsType_textblock")
tnmheader = firstpost.find(string=re.compile("Tamil New Movies"))
tnm = tnmheader.find_next("strong")

nms = str(tnm).split("<br/>")

movie_list = {}

def fun(nm):  
    nm = BeautifulSoup(nm,'lxml')
    name = nm.text.split(' - [')[0]
    links = {}
    for post in nm.find_all('a'):
        post_name = post.text
        post_url = post.attrs['href']
        try:
            post_html=urlopen(post_url)
            post_soup=BeautifulSoup(post_html,'lxml')
            mag_tag = post_soup.find('a',attrs={'href':re.compile('magnet')})
            mag_link = mag_tag.attrs['href']
        except:
            mag_link = None
        links[post_name] = mag_link
        #print("%s:%s => %s"%(name,post_name,mag_link))
    return(name,links)

with Pool(16) as p:
    for name,links in p.map(fun,nms):
        movie_list[name]=links

print(len(movie_list))