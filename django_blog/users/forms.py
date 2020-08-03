from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm

class PasswordChangeForm1(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['new_password2'].help_text += '<ul>'
        self.fields['new_password2'].help_text += '<li>repeate new password</li>'
        self.fields['new_password2'].help_text += '</ul>'

    field_order = ['new_password1', 'new_password2', 'old_password']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta :
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2'] #for order

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta :
        model = Profile
        fields = ['image' , 'bio' , 'location' , 'birthday']

        widgets = {'image': forms.FileInput(attrs={'class': 'custom-file-input', 'type': 'file', 'id': 'imageform'}) , 
                    'birthday':forms.TextInput(attrs={'type': 'date'}) }
