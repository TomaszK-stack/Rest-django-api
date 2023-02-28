from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Tier

class CustomUserCreationForm(UserCreationForm):
    tier = forms.ModelChoiceField(queryset=Tier.objects.all())

    class Meta:
        model = User
        fields = ('username', 'email')