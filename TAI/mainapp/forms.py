from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Document, Message, Card
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import datetime

class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        # First perform the default validation
        super().confirm_login_allowed(user)
        
        now = timezone.now()
        
        # Then check if the user is banned
        
        try:
            userprofile = get_object_or_404(UserProfile,associated_user = user )
            if userprofile and userprofile.time_out_end <= now:
                if userprofile.is_banned:
                    userprofile.is_banned = False
                    userprofile.time_out_end = timezone.make_aware(datetime(2025, 1, 1, 12, 0, 0))
                    userprofile.save()
            elif userprofile and userprofile.is_banned:
                raise forms.ValidationError(
                    f"Your account has been detected to be banned. Please contact support. You will be unbanned at {userprofile.time_out_end}",
                    code='banned',
                )
            else:
                userprofile.is_banned = True
                userprofile.save()
                raise forms.ValidationError(
                    f"Your account has been banned in time_out_end. Please contact support. You will be unbanned at {userprofile.time_out_end}",
                    code='banned',
                )
                
        except UserProfile.DoesNotExist:
            pass

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
 
 # Create a docuemnt from textbox or file (works with empty) 
class DocumentCreateForm(forms.Form):
    title   = forms.CharField(max_length=100)
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':10, 'cols':60}),
        required=False,
        help_text="Either paste text here…"
    )
    file = forms.FileField(
        required=False,
        help_text="…or upload a .txt file"
    )  

class MessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="To"
    )
    
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class BankInfoForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_number','cvv','expiry','cardholder_name']
        widgets = {
            'expiry' : forms.TextInput(attrs={'placeholder' : 'MM/YY'})
        }

