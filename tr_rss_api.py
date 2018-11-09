#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:40:50 2018

@author: guru
"""

from multiprocessing import Pool
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re,rfeed,datetime

url = "http://tamilrockers.ph"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")

firstpost = soup.find(class_="ipsType_textblock")
tnmheader = firstpost.find(string=re.compile("Tamil New Movies"))
tnm = tnmheader.find_next("strong")

nms = str(tnm).split("<br/>")

movie_list = {}
item_list = []

def fun(nm):  
    nm = BeautifulSoup(nm,'lxml')
    name = nm.text.split(' - [')[0]
    data = []
    for post in nm.find_all('a'):
        post_name = post.text
        post_url = post.attrs['href']
        try:
            post_html=urlopen(post_url)
            post_soup=BeautifulSoup(post_html,'lxml')
            mag_tag = post_soup.find('a',attrs={'href':re.compile('magnet')})
            tor_tag = post_soup.find('a',attrs={'title':re.compile('Download attachment')})
            mag_link = mag_tag.attrs['href']
            tor_link = tor_tag.attrs['href']
            data.append((post_name,post_url,tor_link,mag_link))
        except:
            mag_link = None
            tor_link = None
        #print("%s:%s => %s"%(name,post_name,mag_link))
    return(name,data)

with Pool(16) as p:
    for name,data in p.map(fun,nms):
        movie_list[name]= data
        for ptype,purl,torurl,magurl in data:
            item_list.append(rfeed.Item(
                                        title=name+' : '+ptype,
                                        link=purl,
                                        enclosure=rfeed.Enclosure(magurl,10000,'application/x-bittorrent')
                                        ))

#print(len(movie_list))

feed = rfeed.Feed(
    title = "TR RSS Feed",
    description = "Unofficial RSS feed for TR",
    link = "localhost",
    lastBuildDate = datetime.datetime.now(),
    items = item_list)

print(feed.rss())