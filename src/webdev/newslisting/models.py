import datetime

from django.db import models
from django.utils import timezone
#
class Topic(models.Model):
    topic_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
         return self.topic_text
    def was_published_recently(self):
         now = timezone.now()
         return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
#
class Article(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    def __str__(self):
         return self.title

class Quote(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quote = models.CharField(max_length=200)
