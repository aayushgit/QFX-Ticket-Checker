# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:00:48 2018

@author: aayushsharma
"""
from bs4 import BeautifulSoup
import urllib.request

class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener=AppURLOpener()

#news page
home_page='https://www.qfxcinemas.com'
uClient=opener.open(home_page)
#HTML Contents
page_html = uClient.read()
#close connection
uClient.close()
soup=BeautifulSoup(page_html,'lxml')
mylist=['']
#print("Movie To Look For")
#a=input()
for content in soup.find_all('h4'):
    mylist+=(content.text.split('\n'))  

if 'Coming Soon' in mylist:
    mylist=mylist[0:mylist.index('Coming Soon')]

if any ('Infinity' in s for s in mylist):
    print('Yes')
else:
    print('No')    

#Email Here
