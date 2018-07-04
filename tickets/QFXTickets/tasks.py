import celery
from celery import current_app
from celery.schedules import crontab
from celery.task import periodic_task

from .models import NowShowing, Emails
from django.core.mail import EmailMultiAlternatives
from bs4 import BeautifulSoup
import urllib.request


class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


@celery.task
def sendEmail(movietitle):
    from_email = "saneprijal@gmail.com"
    subject = "New Movie Arrival"
    content = "Movie Tickets available for: \n"
    for mv in movietitle:
        movie = NowShowing.objects.get(movie_title=mv)
        content = content + mv + " Booking link:  " + movie.movie_link + "\n"
    print(content)
    mailList = []
    emails = Emails.objects.all()
    for mail in emails:
        mailList.append(mail.email)

    print(mailList)

    msg = EmailMultiAlternatives(subject, content, from_email, bcc=mailList)
    msg.send()
    print("Email sent")


@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="getNowShowing",
    ignore_result=True
)
def getNowShowing():
    print("Hello World")
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
    newmovie = []

    movies = soup.find('div', attrs={'class': 'content'})
    for all_movies in movies.findAll('div', attrs={'class': 'movies'}):
        for movie in all_movies.findAll('div', attrs={'class': 'movie'}):
            a = movie.find('a', attrs={'class': 'ticket'})
            if a:
                ticketlink = a['href']
                h4 = movie.find('h4', attrs={'class': 'movie-title'})
                title = h4.text
                ticketlink = "https://www.qfxcinemas.com" + ticketlink
                ticketbook['title'] = title
                ticketbook['link'] = ticketlink
                nowShowing.append(ticketbook.copy())

            else:
                continue

    for m in nowShowing:
        title = m['title']
        link = m['link']
        try:
            now = NowShowing.objects.get(movie_title=title)
        except NowShowing.DoesNotExist:
            now = None
        if not now:
            new = NowShowing()
            new.movie_title = title
            new.movie_link = link
            new.save()

            newmovie.append(title)
    if newmovie:
        sendEmail.delay(newmovie)
