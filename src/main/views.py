from django.shortcuts import render
from authentication.models import Profile
from discord.models import Topic, Idea, IdeaComment
from django.db.models import Q

# Create your views here.

def home_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    return (
        render(request, 'home.html', {'ideas': Idea.objects.all(), 'topic': Topic.objects.first(), 'comments': IdeaComment.objects.all(), 'profile': profile})
    )
