from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# Home view (landing page)
def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        return render(request, 'main/home.html', {'message': 'Welcome back, {}'.format(request.user.username)})
    else:
        return render(request, 'main/home.html', {'message': 'Welcome to our site!'})
