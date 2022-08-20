
import datetime
import random
from tkinter import END
# from tracemalloc import start

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from authentication.models import Profile
from debate.models import Debate,DebateActor
from authentication.views import NOTIFICATION_TAGS
from .models import Idea, TopicSuggestion, Topic, IdeaComment
from debate.views import DEBATE_TEAMS, get_team_users
import random

# Create your views here.

@login_required
def suggest_topic_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    return render(request, 'suggest_topic.html', {'profile': profile})


def debate_view(request):
    debate = Debate.objects.first()
    start_date, announce_date = debate.debate_start_date, debate.debate_announce_date
    nowtz = datetime.datetime.now().astimezone()
    debate_actor = {}
    if request.user.is_authenticated:
        try:
            debate_actor = DebateActor.objects.get(Q(actor_user_account = request.user))
        except DebateActor.DoesNotExist:
            debate_actor = False 
    diff = (start_date - nowtz)
    days, hours, mins = diff.days, diff.seconds // 3600, (diff.seconds // 60) % 60
    offset = {'days': days, 'hours': hours, 'minutes': mins, 'debate': debate, 'debateactor': debate_actor}
    if announce_date <= nowtz:
        offset['announced'] = True
    if start_date <= nowtz:
        offset['started'] = True 
        end_date = debate.debate_end_date
        diff = (end_date - nowtz)
        days, hours, mins = diff.days, diff.seconds // 3600, (diff.seconds // 60) % 60
        offset['days'] = days 
        offset['hours'] = hours 
        offset['minutes'] = mins 

    if debate_actor:
        if debate_actor.actor_team == 'Belirlenmemiş':
            debate_actor.actor_team = random.choice([*DEBATE_TEAMS.keys()])
            while get_team_users(debate_actor.actor_team) >= 2:
                debate_actor.actor_team = random.choice([*DEBATE_TEAMS.keys()])
            debate_actor.save(update_fields=['actor_team'])
            offset['debateactor'] = debate_actor
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    offset['profile'] = profile
    return render(request, 'debate.html', offset)

@login_required
def send_idea_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    return render(request, 'send_idea.html', {'topic': Topic.objects.first(), 'profile': profile})

@login_required
def suggest_topic_to_server(request):
    if request.method == 'POST':
        topic, keywords = request.POST['topic'].lower(), request.POST['keywords'].lower()
        
        try:
            keywords.split(',')[4]
        except IndexError:
            messages.error(request, 'Anahtar kelimeler doğru formatta değil.', NOTIFICATION_TAGS['error'])
            return render(request, 'suggest_topic.html')

        try:
            TopicSuggestion.objects.filter(Q(topic_name = topic) | Q(topic_keywords = keywords))
        except TopicSuggestion.DoesNotExist:
            messages.error(request, 'Bu konuda bir fikir zaten iletilmiş.', NOTIFICATION_TAGS['error'])
            return render(request, 'suggest_topic.html')
        else:
            try:
                profile = Profile.objects.get(Q(user = request.user))
            except Profile.DoesNotExist:
                messages.error(request, 'Bu hesapla bir öneri yapamazsın.', NOTIFICATION_TAGS['error'])
                return render(request, 'suggest_topic.html')
            else:
                if profile.topic_suggestion_cooldown.replace(tzinfo=None) <= datetime.datetime.now():

                    profile.topic_suggestion_cooldown = datetime.datetime.now() + datetime.timedelta(days=1)
                    profile.save(update_fields=['topic_suggestion_cooldown'])
                else:
                    messages.error(request, f'Şu anda öneri yapamazsın, cooldown.', extra_tags=NOTIFICATION_TAGS['error'])
                    return render(request, 'suggest_topic.html')

            suggestion = TopicSuggestion.objects.create(topic_name = topic, topic_keywords = keywords)
            suggestion.save()

            messages.success(request, 'Konu öneriniz ekibimize ulaştırıldı.', NOTIFICATION_TAGS['success'])

            return render(request, 'suggest_topic.html')

@login_required
def send_idea_to_server(request):
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(Q(user = request.user))
        except Profile.DoesNotExist:
            messages.error(request, 'Bu hesapla bir öneri yapamazsın.', NOTIFICATION_TAGS['error'])
            return render(request, 'send_idea.html')
        else:
            if profile.energy >= 1:

                profile.energy -= 1
                profile.total_ideas += 1
                profile.total_score += 10

                profile.save(update_fields=['energy', 'total_ideas', 'total_score'])

                try:
                    idea = Topic.objects.first()
                except IntegrityError:
                    messages.error(request, 'Müsait bir konu yok.', NOTIFICATION_TAGS['error'])
                    return render(request, 'send_idea.html')
                else:
                    comment = Idea.objects.create(topic = idea, idea_author = request.user, idea_content = request.POST['idea'], comment_publish_date = datetime.datetime.now().strftime('%H.%M'))

                    comment.save()

                    messages.success(request, 'Fikriniz başarıyla paylaşıldı.', NOTIFICATION_TAGS['success'])

                    return redirect('home')
            else:

                messages.error(request, 'Enerjin kalmadı, biraz sonra tekrar uğra!', NOTIFICATION_TAGS['error'])

                return redirect('home')

@login_required
def like_idea_view(request, id: int):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        messages.error(request, 'Bu hesapla bir fikir beğenemezsin.', NOTIFICATION_TAGS['error'])
        return redirect('home')
    else:
        try: 
            idea = Idea.objects.get(Q(id = id))
        except Idea.DoesNotExist:
            messages.error(request, 'Böyle bir fikir bulunamadı.', NOTIFICATION_TAGS['error'])
            return redirect('home')
        else:
            user_liked_ideas = profile.liked_ideas 
            
            idea_author = idea.idea_author
            idea_author_profile = Profile.objects.get(Q(user = idea_author))

            try:
                user_liked_ideas[str(id)]
            except KeyError:
                profile.liked_ideas[str(id)] = True 
                profile.save(update_fields=['liked_ideas'])

                idea.idea_likes += 1
                idea_author_profile.my_idea_likes += 1

                idea.save(update_fields=['idea_likes'])
                idea_author_profile.save(update_fields=['my_idea_likes'])


                messages.info(request, 'Fikir beğenildi.', NOTIFICATION_TAGS['info'])
                return redirect(request.META['HTTP_REFERER'])
            else:
                del profile.liked_ideas[str(id)]
                profile.save(update_fields=['liked_ideas'])

                idea.idea_likes -= 1
                idea.save(update_fields=['idea_likes'])

                messages.info(request, 'Fikirin beğenilmesi alındı.', NOTIFICATION_TAGS['info'])
                return redirect(request.META['HTTP_REFERER'])
                

def inspect_idea_view(request, id: int):
    try: 
        idea = Idea.objects.get(Q(id = id))
    except Idea.DoesNotExist:
        messages.error(request, 'Böyle bir fikir bulunamadı.', NOTIFICATION_TAGS['error'])
        return redirect('home')
    else:
        try:
            profile = Profile.objects.get(Q(user = request.user))
        except Profile.DoesNotExist:
            profile = {'ui_theme': 'tema1'}
        except TypeError:
            profile = {'ui_theme': 'tema1'}
        return render(request, 'inspect_idea.html', {'idea': idea, 'comments': retrieve_idea_comments(idea), 'profile': profile})

def retrieve_idea_comments(idea):

    try:
        comments = IdeaComment.objects.filter(Q(sup_comment = idea))
    except IdeaComment.DoesNotExist:
        return []
    else:
        return comments

@login_required
def comment_idea_view(request, id: int):
    if request.method == 'POST':

        try:
            profile = Profile.objects.get(Q(user = request.user))
        except Profile.DoesNotExist:
            messages.error(request, 'Bu hesapla bir fikir beğenemezsin.', NOTIFICATION_TAGS['error'])
            return redirect('home')
        else:
            try: 
                idea = Idea.objects.get(Q(id = id))
            except Idea.DoesNotExist:
                messages.error(request, 'Böyle bir fikir bulunamadı.', NOTIFICATION_TAGS['error'])
                return redirect('home')
            else:
                try:
                    if not isinstance(profile.commented_ideas[str(id)], list):
                        profile.commented_ideas[str(id)] = []
                except KeyError:
                    profile.commented_ideas[str(id)] = []
                    
                idea.idea_comments += 1
                idea.save(update_fields=['idea_comments'])

                comment = IdeaComment.objects.create(sup_comment = idea, comment_author = request.user, comment_content = request.POST['content'])
                comment.save()

                idea_author = idea.idea_author
                idea_author_profile = Profile.objects.get(Q(user = idea_author))

                idea_author_profile.my_idea_comments += 1
                idea_author_profile.save(update_fields=['my_idea_comments'])

                profile.commented_ideas[str(id)].append(comment.comment_id)
                profile.save(update_fields=['commented_ideas'])
                messages.info(request, 'Fikire yorum yapıldı.', NOTIFICATION_TAGS['info'])
                return redirect(request.META['HTTP_REFERER'])
        
def share_idea_view(request, id: int):
    messages.info(request, 'Fikrin paylaşma bağlantısı kopyalandı', extra_tags=NOTIFICATION_TAGS['info'])
    return redirect(request.META['HTTP_REFERER'])

def trends_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    trend_ideas = Idea.objects.all().order_by('-idea_comments')
    try:
        trend_ideas = trend_ideas[:3]
    except IndexError:
        trend_ideas 

    return render(request, 'trends.html', {'trend_ideas': trend_ideas, 'topic': Topic.objects.first(), 'profile': profile})

def favs_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    ideas = Idea.objects.all().order_by('-idea_likes')
    try:
        ideas = ideas[:3]
    except IndexError:
        ideas 

    return render(request, 'favs.html', {'fav_ideas': ideas, 'topic': Topic.objects.first(), 'profile': profile})

def random_ideas_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    ideas = list(Idea.objects.all())
    try:
        ideas = random.sample(ideas, 3)
    except ValueError:
        ideas

    return render(request, 'random_ideas.html', {'random_ideas': ideas, 'topic': Topic.objects.first(), 'profile': profile})