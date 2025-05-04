from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home_page, sign_up, dashboard, text_editor, user_settings

urlpatterns = [
    path('', home_page, name='home-page'),
    path('sign-up/', sign_up, name='sign_up'),
    path("sign-in/", LoginView.as_view(template_name="mainapp/sign_in.html"), name="sign_in"),
    path('dashboard/', dashboard, name='dashboard'),
    path('text-editor/', text_editor, name='text_editor'),
    path('user-settings/', user_settings, name='user-settings'),
    path('logout', LogoutView.as_view(), name="logout"),
]

