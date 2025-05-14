from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile, Transaction, Card, TokensPackage, Message, Document , Blacklist, Collaborator


# admin.site.register(UserProfile)
admin.site.register(Message)
admin.site.register(Document)
admin.site.register(Blacklist)
admin.site.register(Collaborator)
# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('associated_user', 'tier', 'tokens')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'price', 'card', 'timestamp')
    search_fields = ('user__username', 'package__name')
    list_filter = ('timestamp',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'masked_card_number', 'cardholder_name', 'expiry')
    search_fields = ('user__username', 'cardholder_name')

    def masked_card_number(self, obj):
        return f"**** **** **** {obj.card_number[-4:]}"
    masked_card_number.short_description = 'Card Number'

@admin.register(TokensPackage)
class TokensPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'token_value', 'bv')
    list_filter = ('bv',)
    search_fields = ('names',)