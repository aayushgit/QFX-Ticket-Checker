# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 19:00:48 2018

@author: aayushsharma
"""
from bs4 import BeautifulSoup
import urllib.request

class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def getNowShowing():
    opener = AppURLOpener()

    home_page = 'https://www.qfxcinemas.com'
    uClient = opener.open(home_page)
    # HTML Contents
    page_html = uClient.read()
    # close connection
    uClient.close()

    soup = BeautifulSoup(page_html, "html.parser")
    nowShowing = []
    ticketbook = {}

    movies = soup.find('div', attrs={'class': 'movies'})
    for movie in movies.findAll('div', attrs={'class': 'movie'}):
        a = movie.find('a')
        ticketlink = a['href']
        h4 = movie.find('h4')
        title = h4.text
        ticketbook['title'] = title
        ticketbook['link'] = ticketlink
        nowShowing.append(ticketbook.copy())

    for m in nowShowing:
        print(m['title'] + " " + m['link'])

    print(nowShowing)

if __name__ == '__main__':
    getNowShowing()

