from __future__ import absolute_import, unicode_literals
from .models import NowShowing
from .models import Emails
from celery import task

from bs4 import BeautifulSoup
import urllib.request
class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def sendEmail(movietitle):
    for mv in movietitle:
        movie = NowShowing.objects.get(movie_title=mv)
        emails = Emails.objects.all()
        mailList = emails.email

@task()
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
    newmovie= []

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
        title = m['title']
        link = m['link']
        now = NowShowing.objects.get(movie_title=title)
        if not now:
            new = NowShowing()
            new.movie_title = title
            new.movie_link = link
            new.save()

            newmovie.append(title)

    sendEmail(newmovie)