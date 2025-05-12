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
            return redirect('sign_in')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/sign_up.html', {'form': form})

# experience section
@login_required
def dashboard(request):
    return render(request, 'mainapp/dashboard.html')

@login_required
def text_editor(request):
    return render(request, 'mainapp/text_editor.html')

@login_required
def user_settings(request):
    if request.method == 'POST':
        # Handle settings update
        return redirect('user-settings')
    return render(request, 'mainapp/user_settings.html')

@login_required
def tokens(request):
    return render(request, 'mainapp/tokens.html')

@login_required
def cart(request):
    return render(request, 'mainapp/cart.html')

"""function to load """