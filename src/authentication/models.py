import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

# Create your models here.

UI_THEMES = (
    ('tema1', 'Varsayılan Tema (Mor - Lila)'),
    ('tema2', 'İkincil Tema (Yeşil)'),
    ('tema3', 'Üçüncül Tema (Gri)')
)

class Profile(models.Model):
    id = models.AutoField(primary_key=True)

    phone_number = models.CharField(max_length=10,  validators=[MinLengthValidator(10)])
    phone_verification_token = models.CharField(max_length=6)
    phone_verification_deadline = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None))

    is_phone_verified = models.BooleanField(default=False)

    profile_creation_date = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None))

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    is_mail_verified = models.BooleanField(default=False)
    mail_verification_token = models.CharField(max_length=32, default='')
    mail_verification_deadline = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None))

    topic_suggestion_cooldown = models.DateTimeField(default=datetime.datetime.now().replace(tzinfo=None))

    energy = models.IntegerField(default=5)

    liked_ideas = models.JSONField(default=dict, blank=True)
    commented_ideas = models.JSONField(default=dict, blank=True)

    my_idea_likes = models.IntegerField(default=0)
    my_idea_comments = models.IntegerField(default=0)

    total_ideas = models.IntegerField(default=0)
    current_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    ui_theme = models.CharField(choices=UI_THEMES, default='tema1', blank=False, max_length=10)
