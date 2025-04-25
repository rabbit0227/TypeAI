from django.urls import path
from .views import home_page

urlpatterns = [
    path('', home_page, name='home-page'),
    # path('signup/', views.signup, name='signup'),
    # path('login/', views.login_view, name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
]