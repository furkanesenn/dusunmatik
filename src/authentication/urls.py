from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('register', register_view),
    path('attemptregister', register_attempt_view),
    path('login', login_view, name = 'login'),
    path('attemptlogin', login_attempt_view),
    path('logout', logout_view),
    # path('forgotpassword', forgotpassword_view),
    re_path(r'^verifymail/(?P<token>.{32})', verifymail_view),
    re_path('profile/(?P<profile_user>.*)', profile_view, name = 'profile'),
    path('resendverification', resend_mail_verification),
    path('phonenumberverification', phone_number_verification)
]

