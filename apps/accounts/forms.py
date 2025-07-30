from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ContactMessage

#Signup User Form
class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture')

#Edit Profile Form
class CustomUserChangeForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture')

# Contact Us Form
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']

