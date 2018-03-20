from django.forms import Form, ModelForm
from django.conf import settings
from django import forms
from main.models import UserProfile, Action

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    age = forms.IntegerField(required=True)
    gender = forms.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'bio', 'age', 'gender']


class ActionForm(ModelForm):
    other_person_user_id = forms.IntegerField(required=True)
    like = forms.ChoiceField(choices=BOOL_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = Action
        fields = ['other_person_user_id', 'like']
