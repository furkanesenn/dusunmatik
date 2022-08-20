import datetime
# from fcntl import F_SEAL_SEAL 

from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

def get_default_date():
    today = datetime.datetime.now()
    sunday = today + datetime.timedelta( (4-today.weekday()) % 7 )
    return sunday

class Debate(models.Model):
    debate_id = models.AutoField(primary_key=True)

    debate_topic = models.CharField(max_length=50)
    debate_description = models.TextField(default='')
    debate_keywords = models.CharField(max_length=50)


    debate_start_date = models.DateTimeField(default=get_default_date())
    debate_announce_date = models.DateTimeField(default=get_default_date() - datetime.timedelta(hours = 1))
    debate_end_date = models.DateTimeField(default=get_default_date() + datetime.timedelta(hours=3))

class DebateActor(models.Model):
    actor_id = models.AutoField(primary_key=True)

    actor_user_account = models.ForeignKey(to = User, on_delete=models.CASCADE)
    actor_team = models.CharField(max_length=15)

class DebateRoom(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(User, help_text="Users who are connected")

    def __str__(self):
        return self.title 
    
    def connect_user(self, user):
        is_user_added = False 
        if user not in self.user.all():
            self.users.add(user)
            self.save()
            is_user_added = True 
        elif user in self.users.all():
            is_user_added = True 
        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False 
        if user not in self.user.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True 
        return is_user_removed

    @property 
    def group_name(self):
        return f"DebateRoom-{self.id}"

class DebateRoomMessageManager(models.Manager):
    def by_room(self, room):
        qs = DebateRoomMessage.objects.filter(room = room).order_by('-timestamp')
        return qs 

class DebateRoomMessage(models.Model):
    user = models.ForeignKey(to = User, on_delete=models.CASCADE)
    room = models.ForeignKey(DebateRoom, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(unique=False, blank=False)

    objects = DebateRoomMessageManager()

    def __str__(self): return self.content