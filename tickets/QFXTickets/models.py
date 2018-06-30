from django.db import models

class Emails(models.Model):
    email = models.CharField(max_length=100)

class NowShowing(models.Model):
    movie_title = models.CharField(max_length=255)
    movie_link = models.CharField(max_length=255)

