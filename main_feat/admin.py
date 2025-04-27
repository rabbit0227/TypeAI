from django.contrib import admin

# Register your models here.
from .models import Accounts, Payment, Mailbox, Doc, Collaborator, Complaint, Blacklist

admin.site.register(Accounts)
admin.site.register(Payment)
admin.site.register(Mailbox)
admin.site.register(Doc)
admin.site.register(Collaborator)
admin.site.register(Complaint)
admin.site.register(Blacklist)
