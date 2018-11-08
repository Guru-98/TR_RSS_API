#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 12:40:50 2018

@author: guru
"""

from multiprocessing import Pool
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import sqlite3

conn = sqlite3.connect('TR_Links.db')
url = "http://tamilrockers.by"

def getSoupFromLink(_url):
    req = Request(_url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req)
    _soup = BeautifulSoup(html, "lxml")
    return _soup

def executeSql(sql_command):
    c = conn.cursor()
    c.execute(sql_command)
    conn.commit()

def getMagLink(post_url):
    try:
        post_soup=getSoupFromLink(post_url)
        mag_tag = post_soup.find('a',attrs={'href':re.compile('magnet')})
        mag_link = mag_tag.attrs['href']
    except:
        mag_link = None

    return mag_link

def insertMovie(_name, _post_name, _mag_link):
    executeSql('''INSERT INTO movies VALUES ('%s', '%s', '%s')'''
               %(_name, _post_name, _mag_link))

def fetchMagLinks(_nm):
    nm = BeautifulSoup(_nm,'lxml')
    name = nm.text.split(' - [')[0]
    anchors = nm.find_all('a')

    for post in anchors:
        post_name = post.text
        post_url = post.attrs['href']
        mag_link = getMagLink(post_url)
        if mag_link:
            insertMovie(name, post_name, mag_link)

soup = getSoupFromLink(url)

executeSql('''CREATE TABLE movies
              (movie_name text, post_name text, mag_link text)''')

firstpost = soup.find(class_="ipsType_textblock")
tnmheader = firstpost.find(string=re.compile("Tamil New Movies"))
tnm = tnmheader.find_next("strong")

nms = str(tnm).split("<br/>")

pool = Pool(processes=4)
results = pool.map(fetchMagLinks, nms)
conn.close()
