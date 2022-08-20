from django.contrib import admin
from django.urls import path, re_path, include
from .views import *

# app_name = 'main'

urlpatterns = [
    path('', home_view, name = 'home'),
    re_path(r'^auth/', include('authentication.urls') , name = 'auth'),
    re_path(r'^discord/', include('discord.urls') , name = 'discord'),
    re_path(r'^debate/', include('debate.urls') , name = 'debate'),
]

