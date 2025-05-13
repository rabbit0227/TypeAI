from django.contrib import admin
from .models import Message, Document, UserProfile, Blacklist, Collaborator

admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Document)
admin.site.register(Blacklist)
admin.site.register(Collaborator)
# Register your models here.
