from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Q 

from authentication.views import NOTIFICATION_TAGS
from .models import Debate, DebateActor

DEBATE_TEAMS = {
    'Hükümet 1': [],
    'Hükümet 2': [],
    'Muhalefet 1': [],
    'Muhalefet 2': []
}

# Create your views here.

@login_required
def apply_debate_view(request):
    debate_actors = DebateActor.objects.all()
    if len(debate_actors) < 8:
        try:
            DebateActor.objects.get(Q(actor_user_account = request.user))
        except DebateActor.DoesNotExist:
            DebateActor.objects.create(actor_user_account = request.user, actor_team = 'Belirlenmemiş') 
        
            messages.success(request, 'Başarıyla münazaraya katıldın!', NOTIFICATION_TAGS['success'])

            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Zaten bu münazarada varsın.', extra_tags=NOTIFICATION_TAGS['error'])
            return redirect(request.META['HTTP_REFERER'])
    else:
        messages.error(request, 'Kontenjan dolmuş (8/8).', extra_tags=NOTIFICATION_TAGS['error'])
        return redirect(request.META['HTTP_REFERER'])

def get_team_users(team_name: str) -> int:
    try:
        DEBATE_TEAMS[team_name]
    except KeyError: return -1
    else:
        try:
            team_users = DebateActor.objects.filter(Q(actor_team = team_name))
        except DebateActor.DoesNotExist: return 0
        else:
            return len(team_users)

@login_required
def start_debate_view(request): pass