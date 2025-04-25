from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages

# Create your views here.
# Home view (landing page)
def home_page(request):
    return render(request, 'mainapp/home.html')
