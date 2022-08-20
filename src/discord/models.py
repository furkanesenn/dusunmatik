import datetime

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

IDEA_GENRES = (
    ('trend', 'TREND'),
    ('fashion', 'FASHION')
)

class Topic(models.Model):
    id = models.AutoField(primary_key=True)
    
    idea_name = models.CharField(max_length=100)
    idea_description = models.TextField()
    idea_genre = models.CharField(max_length=10, choices=IDEA_GENRES, default='trend')

    idea_deadline = models.DateTimeField(default=datetime.datetime.now())

class TopicSuggestion(models.Model):
    id = models.AutoField(primary_key=True)

    topic_name = models.CharField(max_length=40)
    topic_keywords = models.CharField(max_length=50)

class Idea(models.Model):
    id = models.AutoField(primary_key=True)

    topic = models.ForeignKey(to = Topic, on_delete=models.CASCADE)

    idea_author = models.ForeignKey(to = User, on_delete=models.CASCADE)
    idea_content = models.TextField()

    idea_likes = models.IntegerField(default=0)
    idea_comments = models.IntegerField(default=0)

    comment_publish_date = models.CharField(max_length=6)

class IdeaComment(models.Model):
    comment_id = models.AutoField(primary_key=True)

    sup_comment = models.ForeignKey(to = Idea, on_delete=models.CASCADE)
    
    comment_author = models.ForeignKey(to = User, on_delete=models.CASCADE)
    comment_content = models.TextField()
