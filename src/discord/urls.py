from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('suggest_topic', suggest_topic_view),
    path('debate', debate_view),
    path('send_idea', send_idea_view),
    path('trends', trends_view),
    path('favourites', favs_view),
    path('random_ideas', random_ideas_view),
    path('suggest_topic_to_server', suggest_topic_to_server),
    path('send_idea_to_server', send_idea_to_server),
    path('like_idea/<int:id>', like_idea_view),
    path('inspect_idea/<int:id>', inspect_idea_view),
    path('comment_idea/<int:id>', comment_idea_view),
    path('share_idea/<int:id>', share_idea_view),
]

