# from mimetypes import MimeTypes
import smtplib, ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import hashlib
import random
import datetime
import threading
import time 

from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from django.http import HttpResponseNotFound

from sms import send_sms

from .models import Profile
from .forms import EditAccountForm, EditProfileForm, ChangeAccountPassword

EMAIL_CREDENTIALS = {
    'email_address': 'jthink011@gmail.com',
    'email_password': 'rvlwjpjyeqmucdsd'
}

NOTIFICATION_TAGS = {
    'success': 'check_circle',
    'error': 'error',
    'warning': 'warning',
    'info': 'info'
}

EMAIL_CONTENT = {
    'head': '<!DOCTYPE html> <html> <head> <meta charset="utf-8"> <meta http-equiv="x-ua-compatible" content="ie=edge"> <title>Email Confirmation</title> <meta name="viewport" content="width=device-width, initial-scale=1"> <style type="text/css"> /** * Google webfonts. Recommended to include the .woff version for cross-client compatibility. */ @media screen { @font-face { font-family: "Source Sans Pro"; font-style: normal; font-weight: 400; src: local("Source Sans Pro Regular"), local("SourceSansPro-Regular"), url(https://fonts.gstatic.com/s/sourcesanspro/v10/ODelI1aHBYDBqgeIAH2zlBM0YzuT7MdOe03otPbuUS0.woff) format("woff"); } @font-face { font-family: "Source Sans Pro"; font-style: normal; font-weight: 700; src: local("Source Sans Pro Bold"), local("SourceSansPro-Bold"), url(https://fonts.gstatic.com/s/sourcesanspro/v10/toadOcfmlt9b38dHJxOBGFkQc6VGVFSmCnC_l7QZG60.woff) format("woff"); } } /** * Avoid browser level font resizing. * 1. Windows Mobile * 2. iOS / OSX */ body, table, td, a { -ms-text-size-adjust: 100%; /* 1 */ -webkit-text-size-adjust: 100%; /* 2 */ } /** * Remove extra space added to tables and cells in Outlook. */ table, td { mso-table-rspace: 0pt; mso-table-lspace: 0pt; } /** * Better fluid images in Internet Explorer. */ img { -ms-interpolation-mode: bicubic; } /** * Remove blue links for iOS devices. */ a[x-apple-data-detectors] { font-family: inherit !important; font-size: inherit !important; font-weight: inherit !important; line-height: inherit !important; color: inherit !important; text-decoration: none !important; } /** * Fix centering issues in Android 4.4. */ div[style*="margin: 16px 0;"] { margin: 0 !important; } body { width: 100% !important; height: 100% !important; padding: 0 !important; margin: 0 !important; } /** * Collapse table borders to avoid space between cells. */ table { border-collapse: collapse !important; } a { color: #1a82e2; } img { height: auto; line-height: 100%; text-decoration: none; border: 0; outline: none; } body { background-color: #e9ecef; } td.header { padding: 36px 24px 0; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; border-top: 3px solid #d4dadf; } td.header h1 { margin: 0; font-size: 32px; font-weight: 700; letter-spacing: -1px; line-height: 48px; } .toptable {max-width: 600px;} .ndtable .ndtd {padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;} .ndtd p {margin: 0;} .startbtntd {padding: 12px;} .startbtntd td {border-radius: 6px} p {margin: 0;} .startbtntd a {display: inline-block; padding: 16px 36px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; color: #ffffff; text-decoration: none; border-radius: 6px;} .copybtntd {padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px;} .copybtntd p {margin: 0;} .cheerstd {padding: 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 16px; line-height: 24px; border-bottom: 3px solid #d4dadf} .cheerstd p {margin: 0;} .footer {padding: 24px;} .footertable {max-width: 600px} .styleatt {padding: 12px 24px; font-family: "Source Sans Pro", Helvetica, Arial, sans-serif; font-size: 14px; line-height: 20px; color: #666;} </style> </head>',
    'body': '<body>  <table border="0" cellpadding="0" cellspacing="0" width="100%">  <tr> <td align="center" bgcolor="#e9ecef">   </td> </tr>   <tr> <td align="center" bgcolor="#e9ecef">  <table class="toptable" border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td class="header" align="left" bgcolor="#ffffff"> <h1>Confirm Your Email Address</h1> </td> </tr> </table>  </td> </tr>   <tr> <td align="center" bgcolor="#e9ecef">  <table class="toptable ndtable" border="0" cellpadding="0" cellspacing="0" width="100%">  <tr> <td class="ndtd" align="left" bgcolor="#ffffff"> <p>Tap the button below to confirm your email address. If you didn"t create an account with <a href="https://blogdesire.com">Justhink</a>, you can safely delete this email.</p> </td> </tr>   <tr> <td align="left" bgcolor="#ffffff"> <table border="0" cellpadding="0" cellspacing="0" width="100%"> <tr> <td class="startbtntd" align="center" bgcolor="#ffffff"> <table border="0" cellpadding="0" cellspacing="0"> <tr> <td align="center" bgcolor="#1a82e2"> <a href="http://{0}" target="_blank">Verify Your Email</a> </td> </tr> </table> </td> </tr> </table> </td> </tr>   <tr> <td class="copybtntd" align="left" bgcolor="#ffffff" > <p>If that doesn"t work, copy and Justhink the following link in your browser:</p> <p><a href="{0}" target="_blank">{0}</a></p> </td> </tr>   <tr> <td class="cheerstd" align="left" bgcolor="#ffffff"> <p>Cheers,<br> Justhink</p> </td> </tr>  </table>  </td> </tr>   <tr> <td class="footer" align="center" bgcolor="#e9ecef">  <table border="0" cellpadding="0" cellspacing="0" width="100%" class="footertable">  <tr> <td align="center" bgcolor="#e9ecef" class="styleatt"> <p >You received this email because we received a request for email verification request for your account. If you didn"t request that verification you can safely delete this email.</p> </td> </tr>   <tr> <td align="center" bgcolor="#e9ecef" class="styleatt"> <p>Justhink 1234. Beşiktaş, İstanbul, Türkiye</p> </td> </tr>  </table>  </td> </tr>  </table>  </body> </html>'
}

# Create your views here.


def register_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    return (
        render(request, 'register.html', {'profile': profile})
    )

def register_attempt_view(request):
    if not request.user.is_authenticated and request.method == 'POST':
        username, email, password, repassword = request.POST['username'], request.POST['email'], request.POST['password'], request.POST['repassword'] 
        try:
            validate_email(email)
        except ValidationError as err:
            return render(request, 'register.html', {'error': 'Email is not true'})
        else:
            try:
                target_element = User.objects.get(Q(username = username) | Q(email = email))
                return render(request, 'register.html', {'error': 'This credentials already matches with another user'})
            except User.DoesNotExist:
                user = User.objects.create_user(username = username, email = email, password = password)
                token = send_email_verification(email)
                acc = Profile.objects.create(user = user, is_mail_verified = False, mail_verification_token = token, mail_verification_deadline = datetime.datetime.now() + datetime.timedelta(minutes=30))
                messages.success(request, f'Yeni hesabınız oluşturuldu: {username}', extra_tags=NOTIFICATION_TAGS['success'])
                return login_attempt_view(request)
    else:
        return render(request, 'register.html', {'error': 'You already logged in'})
            
def login_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    return (
        render(request, 'login.html', {'profile': profile})
    )

def login_attempt_view(request):
    if not request.user.is_authenticated and request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)

            energy_thread = threading.Thread(target = increment_energy, args=(request))

            energy_thread.start()

            messages.success(request, f'Başarıyla hesabına giriş yaptın: {username}', NOTIFICATION_TAGS['success'])
            return redirect('home')
        else:
            return redirect('login')
    else:
        return redirect('login')

def increment_energy(request):
    while request.user.is_active and request.user.is_authenticated:
        time.sleep(15 * 60)
        try:
            profile = Profile.objects.get(Q(user = request.user))
        except Profile.DoesNotExist:
            pass 
        else: 
            if profile.energy < 20:
                profile.energy += 1
                profile.save(update_fields=['energy'])

@login_required
def logout_view(request):
    messages.success(request, f'Hesaptan çıkış yapıldı: {request.user.username}', NOTIFICATION_TAGS['success'])
    logout(request)
    return redirect('home')
    
@login_required
def resend_mail_verification(request):
    profile = Profile.objects.get(Q(user = request.user))
    token = send_email_verification(request.user.email)
    profile.mail_verification_token = token 
    profile.mail_verification_deadline = datetime.datetime.now() + datetime.timedelta(minutes=30)
    profile.save(update_fields=['mail_verification_token', 'mail_verification_deadline'])
    return redirect(request.META['HTTP_REFERER'])

def send_email_verification(target_email: str):    

    email_message = MIMEMultipart()
    email_message['From'] = EMAIL_CREDENTIALS['email_address']
    email_message['To'] = target_email
    email_message['Subject'] = 'Verify your email | Justhink Community'

    random_code = hashlib.md5(str(random.randrange(100000, 999999)).encode()).hexdigest()

    
    html_code = EMAIL_CONTENT['head'] + EMAIL_CONTENT['body'].format(f'localhost:8000/auth/verifymail/{random_code}')

    email_message.attach(MIMEText(html_code, 'html'))

    email_string = email_message.as_string()

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as server:
        server.login(EMAIL_CREDENTIALS['email_address'], EMAIL_CREDENTIALS['email_password'])
        server.sendmail(EMAIL_CREDENTIALS['email_address'], target_email, email_string)

        return random_code

@login_required
def verifymail_view(request, token):
    try:
        user_profile = Profile.objects.get(Q(user = request.user) )
    except Profile.DoesNotExist:
        return render(request, 'home.html', {'error': 'Unknown error occured due to server.'})
    else:
        if user_profile.mail_verification_token == token:
            now = datetime.datetime.now()
            if user_profile.mail_verification_deadline.replace(tzinfo=None) >= now:
                user_profile.is_mail_verified = True
                user_profile.save(update_fields=['is_mail_verified'])
                return redirect('profile', profile_user = '')
            else:
                return render(request, 'home.html', {'error': 'Invalid token'})

@login_required 
def profile_view(request, profile_user):
    if profile_user == 'edit_profile':
        return edit_profile_view(request)
    elif profile_user == 'edit_account':
        return edit_account_view(request)
    elif profile_user == 'change_password':
        return change_password_view(request)
    username = profile_user if profile_user != '' else request.user.username
    try:
        user = User.objects.get(Q(username = username))
        user_profile = Profile.objects.get(Q(user = user))
    except User.DoesNotExist:
        return HttpResponseNotFound('Böyle bir kullanıcı sistemde kayıtlı değil.')
    except Profile.DoesNotExist:
        return HttpResponseNotFound('Bu kullanıcının profilini görüntüleyemezsin.')
    else:
        return render(request, 'profile.html', {'username': username, 't_user': user, 'profile': user_profile})

def edit_profile_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    form = EditProfileForm(instance=profile)
    context = {'form': form, 'profile': profile, 'username': request.user.username}
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', profile_user = '')
    else:
        return render(request, 'edit_profile.html', context)

def edit_account_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    form = EditAccountForm(instance=request.user)
    context = {'form': form, 'profile': profile, 'username': request.user.username}
    
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', profile_user = '')
    else:
        return render(request, 'edit_account.html', context)
@login_required
def change_password_view(request):
    try:
        profile = Profile.objects.get(Q(user = request.user))
    except Profile.DoesNotExist:
        profile = {'ui_theme': 'tema1'}
    except TypeError:
        profile = {'ui_theme': 'tema1'}
    form = ChangeAccountPassword(request.user)
    context = {'form': form, 'profile': profile, 'username': request.user.username}
    
    if request.method == 'POST':
        form = ChangeAccountPassword(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return redirect('profile', profile_user = '')
    else:
        return render(request, 'edit_account.html', context)

@login_required
def phone_number_verification(request):
    profile = Profile.objects.get(Q(user = request.user))
    random_code = str(random.randint(100000, 999999))
    send_sms(
        f'Justhink\'e hoş geldin {request.user.username}!\nTelefon Onay Kodun: {random_code}',
        '+905465952986',
        [f'+90{str(profile.phone_number)}'],
        fail_silently=False,
    )