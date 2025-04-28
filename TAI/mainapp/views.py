from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages
from .forms import SignUpForm
from .models import UserProfile

# Create your views here.
# Home view (landing page)
def home_page(request):
    return render(request, 'mainapp/home.html')

# user section

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/sign_up.html', {'form': form})

# experiance section
@login_required
def dashboard(request):
    return render(request, 'mainapp/dashboard.html')

@login_required
def text_editor(request):
    return render(request, 'mainapp/text_editor.html')

@login_required
def settings(request):
    if request.method == 'POST':
        # Handle settings update
        return redirect('settings')
    return render(request, 'mainapp/settings.html')

