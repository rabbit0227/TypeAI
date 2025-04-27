from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages
from .forms import SignUpForm, TierChangeForm
from .models import Tier, UserProfile

# Create your views here.
# Home view (landing page)
def home_page(request):
    return render(request, 'mainapp/home.html')

# user section

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            free_tier = Tier.objects.get(name='Free')
            UserProfile.objects.create(user=user, tier=free_tier)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/sign_up.html', {'form': form})

def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
    else:
        form = SignInForm()
    return render(request, 'mainapp/sign_in.html', {'form': form})
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

def logout_view(request):
    logout(request)
    return redirect('home')