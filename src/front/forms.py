# forms.py (dans ton app, par exemple "users")

from allauth.account.forms import SignupForm
from django import forms
from quiz.models import UserProfile

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
