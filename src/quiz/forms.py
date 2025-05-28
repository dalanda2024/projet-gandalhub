from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    photo = forms.ImageField(required=False, label="Photo de profil")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'photo']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(user=user, photo=self.cleaned_data.get('photo'))
        return user

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']