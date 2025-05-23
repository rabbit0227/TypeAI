from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import home_page, sign_up, dashboard, text_editor, user_settings
from .views import create_document, save_document, get_document
from .views import inbox, message_detail, send_message, delete_message, get_unread_count, handle_invitation
from .views import tokens, cart, upgrade_user, select_package
from .views import CustomLoginView

urlpatterns = [
    path('', home_page, name='home-page'),
    path('sign-up/', sign_up, name='sign_up'),
    path("sign-in/", CustomLoginView.as_view(template_name="mainapp/sign_in.html"), name="sign_in"),
    path('dashboard/', dashboard, name='dashboard'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    
    # We need to remove this in other HTML stuff
    path('text-editor/', text_editor, name='text_editor'),
    path('settings/', user_settings, name='user_settings'),
    path('logout', LogoutView.as_view(), name="logout"),
    path('docs/new/', create_document, name='create_document'),
    path('docs/<int:pk>/edit/', text_editor,    name='text_editor'),
    path('api/docs/<int:pk>/', get_document, name='get_document'),
    path('api/docs/<int:pk>/save/', save_document, name='save_document'),


    # Inbox URLs, names are subject to change in further design
    path('inbox/', inbox, name='inbox'),
    path('inbox/message/<int:message_id>/', message_detail, name='message_detail'),
    path('inbox/compose/', send_message, name='send_message'),
    path('inbox/delete/<int:message_id>/', delete_message, name='delete_message'),
    path('inbox/unread-count/', get_unread_count, name='get_unread_count'),
    path('message/invitation/<int:message_id>/<str:action>/', handle_invitation, name='handle_invitation'),

    path('tokens/', tokens, name='tokens_landing'),
    path('cart/', cart, name='payment_cart'),
    path('upgrade/', upgrade_user, name='upgrade_user'),
    path('<int:package_id>/', select_package, name='select_package'),

    # ai api
    path('api/blacklist/', get_blacklist, name='get_blacklist'),
    path('api/correct-text/', correct_text, name='correct_text'),
]
