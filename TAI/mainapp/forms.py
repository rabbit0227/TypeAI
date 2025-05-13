from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Card

class SignUpForm(UserCreationForm):
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        profile = UserProfile(associated_user=user)
        profile.save()

        return user

class BankInfoForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number','cvv','expiry','cardholder_name']
        widgets = {
            'expiry' : forms.TextInput(attrs={'placeholder' : 'MM/YY'})
        }

"""
Forms I think I'll need:
Form that'll handle orders and credit/debit card saves as well as updating DB to paid user
Form that'll push to db the updated tokens amount
"""
