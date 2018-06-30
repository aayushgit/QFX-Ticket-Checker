from __future__ import absolute_import, unicode_literals
from celery import task

@task()
def add():
    print(2 + 3)