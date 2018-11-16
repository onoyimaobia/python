from django import  forms
from .models import Videos
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import  User

class SubmitLast(forms.Form):
    url = forms.URLField()

class VideoForm(forms.ModelForm):
    class Meta:
        model= Videos
        fields=  ["videofile","audio"]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30,required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


