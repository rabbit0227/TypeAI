from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Document, Message, Card

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

