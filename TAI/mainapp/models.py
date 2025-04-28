from django.db import models
from django.contrib.auth.models import User
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

    def __str__(self):
        return f"{self.user.username}'s profile"
# }

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
