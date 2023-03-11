
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from blog.models import Profile, Comment
# Create your forms here.


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required') 
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'image']

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'comment']

    def __init__(self, *args, **kwargs):
        """Save the request with the form so it can be accessed in clean_*()"""
        self.request = kwargs.pop('request', None)
        super(CommentPostForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        """Make sure people don't use my name"""
        data = self.cleaned_data['title']
        return data