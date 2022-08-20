from django.contrib import admin
from .models import Idea, IdeaComment, Topic, TopicSuggestion

admin.site.register(Topic)
admin.site.register(TopicSuggestion)
admin.site.register(Idea)
admin.site.register(IdeaComment)