from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from django import forms

## Custom Form for folder creation linking it to the user
class CreateFileForm(forms.ModelForm):
    ## Standard Entries
    class Meta:
        model = Post
        fields = ['title', 'author']
