from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('apply_now', apply_debate_view),
    path('start_now', start_debate_view)
]

