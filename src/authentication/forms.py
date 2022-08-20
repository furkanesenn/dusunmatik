from django.forms import ModelForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.auth.models import User

class EditProfileForm(ModelForm):
    class Meta:
        model = Profile 
        fields = ('ui_theme', 'phone_number')
        labels = {
            'ui_theme': ('Site Arayüz Teması'),
            'phone_number': ('Telefon Numarası')
        }

class EditAccountForm(ModelForm):
    class Meta:
        model = User 
        fields = ('username', 'email')
        labels = {
            'username': ('Kullanıcı Adı'),
            'email': ('E-Posta Adresi'),
        }

class ChangeAccountPassword(PasswordChangeForm):
    class Meta:
        model = User 
