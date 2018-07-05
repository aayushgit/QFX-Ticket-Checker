import celery
from celery.schedules import crontab
from celery.task import periodic_task
from .models import NowShowing, Emails
from django.core.mail import send_mail
from bs4 import BeautifulSoup
import urllib.request


class AppURLOpener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

# task to send email to all subscribers about the booking available for new movies
@celery.task
def sendEmail(movietitle):
    from_email = "saneprijal@gmail.com"
    subject = "New Movie Arrival"
    content = "Movie Tickets available for: \n"
    # set the contents
    for mv in movietitle:
        movie = NowShowing.objects.get(movie_title=mv)
        content = content + mv + " Booking link:  " + movie.movie_link + "\n"

    mailList = []
    # get all the subscribers' mail
    emails = Emails.objects.all()
    for mail in emails:
        mailList.append(mail.email)

    # send mail to all subscribers
    send_mail(subject, content, from_email, mailList, fail_silently=False)


@periodic_task(
    run_every=(crontab(minute='*/5')),
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
    newmovie = []

    movies = soup.find('div', attrs={'class': 'content'})
    for all_movies in movies.findAll('div', attrs={'class': 'movies'}):
        for movie in all_movies.findAll('div', attrs={'class': 'movie'}):
            a = movie.find('a', attrs={'class': 'ticket'})
            # if the movie contains a ticket booking link then
            if a:
                ticketlink = a['href']
                h4 = movie.find('h4', attrs={'class': 'movie-title'})
                title = h4.text
                ticketlink = "https://www.qfxcinemas.com" + ticketlink
                ticketbook['title'] = title
                ticketbook['link'] = ticketlink
                nowShowing.append(ticketbook.copy())

            #if no ticket booking link is found, then ignore the movie
            else:
                continue

    #for each new movie available for booking
    for m in nowShowing:
        title = m['title']
        link = m['link']
        #check if the movie is already stored
        try:
            now = NowShowing.objects.get(movie_title=title)
        except NowShowing.DoesNotExist:
            now = None

        #if movie information not stored previously
        if not now:
            new = NowShowing()
            new.movie_title = title
            new.movie_link = link
            new.save()

            newmovie.append(title)

    #if new movie arrved
    if newmovie:
        #start task sendEmail
        sendEmail.delay(newmovie)
