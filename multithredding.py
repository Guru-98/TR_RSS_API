#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 21:02:03 2018

@author: guru
"""

from urlparse import urlparse
from threading import Thread
import httplib, sys
from queue import Queue

concurrent = 200

def doWork():
    while not q.empty():
        url = q.get()
        status, url = getmaglink(url)
        doSomethingWithResult(status, url)
        q.task_done()

def getStatus(ourl):
    try:
        url = urlparse(ourl)
        conn = httplib.HTTPConnection(url.netloc)
        conn.request("HEAD", url.path)
        res = conn.getresponse()
        return res.status, ourl
    except:
        return "error", ourl

def doSomethingWithResult(status, url):
    print(status, url)

q = Queue(concurrent * 2)
for url in open('urllist.txt'):
        q.put(url.strip())
q.join()

try:
    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()
except KeyboardInterrupt:
    sys.exit()
