from celery.schedules import crontab
from celery.task import periodic_task

from .models import NowShowing, Emails
from django.core.mail import send_mass_mail
from bs4 import BeautifulSoup
import urllib.request
class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def sendEmail(movietitle):
    if movietitle:
        messages = []
        subject = "New Movie Arrival"
        content = "Movie Tickets available for \n"
        for mv in movietitle:
            movie = NowShowing.objects.get(movie_title=mv)
            content = content + mv + " Book at:  " + movie.movie_link

        mailList=[]

        emails = Emails.objects.all()
        for mail in emails:
            mailList.append(mail.email)
        for i in range(len(mailList)):
            messages = (subject, content, mailList[i])

        send_mass_mail(messages, fail_silently=False)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="getNowShowing",
    ignore_result=True
)

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

    sendEmail(newmovie)