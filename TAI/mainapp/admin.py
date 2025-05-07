from django.contrib import admin
from .models import Message, Document, UserProfile

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Document)
# Register your models here.
