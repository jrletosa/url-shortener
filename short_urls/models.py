from django.db import models

MAX_URL_LENGTH = 1024

''' UrlPair moldel to store:
  * long_url: original URL introduced as input
  * short_url: generated URL
'''
class UrlPair(models.Model):
    short_url = models.CharField(max_length=MAX_URL_LENGTH)
    long_url = models.CharField(max_length=MAX_URL_LENGTH)

    @classmethod
    def create(cls, short_url, long_url):
        url = cls(short_url=short_url, long_url=long_url)
        return url

