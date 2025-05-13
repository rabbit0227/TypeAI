from django.db import models
from django.contrib.auth.models import User
from .validators import validate_card_number, validate_expiry, validate_cvv
# from django.core.validators import MaxValueValidator
# added scection {

class UserProfile(models.Model):
    class Tier(models.TextChoices):
        FREE = 'Free', 'Free'
        PAID = 'Paid', 'Paid'
        SUPER = 'Super', 'Super'


    associated_user = models.OneToOneField(User, on_delete=models.CASCADE)

    tier = models.CharField(
        max_length=10,
        choices=Tier.choices,
        default=Tier.FREE
    )

    tokens = models.PositiveIntegerField(
        default=20
    )

    def __str__(self):
        return f"{self.associated_user.username}'s profile"

class Card(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )
    card_number = models.CharField(
        max_length=19, 
        validators=[validate_card_number]
    ) # max length for most cards, min being 13
    cvv = models.CharField(
        max_length=4, 
        validators=[validate_cvv]
        ) # max CVV num possible, AMEX cards
    expiry = models.CharField(
        max_length=5,
        validators=[validate_expiry]
    ) # MM/YY
    cardholder_name = models.CharField(max_length=256)

    def __str__(self):
        return f"Card ending in {self.card_number[-4:]}" # Returning only last 4 digits

class TokensPackage(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=5, 
        decimal_places=2
    ) # Max : 999.99
    token_value = models.PositiveIntegerField()
    bv = models.BooleanField(default=False)
    
    # @classmethod
    # def best_value_package(cls):
    #     return cls.objects.filter(bv=True).first()

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    package = models.CharField(max_length=256)
    # package = models.ForeignKey(
    #     TokensPackage,
    #     on_delete=models.SET_NULL,
    #     null=True
    # )
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    ) # nullable for non card payments
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction by {self.user.username} for {self.price} at {self.timestamp}"

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
