from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home_page, sign_up, dashboard, text_editor, settings, create_document

urlpatterns = [
    path('', home_page, name='home-page'),
    path('sign-up/', sign_up, name='sign_up'),
    path("sign-in/", LoginView.as_view(template_name="mainapp/sign_in.html"), name="sign_in"),
    path('dashboard/', dashboard, name='dashboard'),
    # We need to remove this in other HTML stuff
    path('text-editor/', text_editor, name='text_editor'),
    path('settings/', settings, name='settings'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('docs/new/', create_document, name='create_document'),
    path('docs/<int:pk>/edit/', text_editor,    name='text_editor'),
]

