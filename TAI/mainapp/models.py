from django.db import models
from django.contrib.auth.models import User
# added scection {
class Tier(models.Model):
    NAME_CHOICES = (
        ('Free', 'Free'),
        ('Pro', 'Pro'),
        ('Enterprise', 'Enterprise'),
    )
    name = models.CharField(max_length=20, choices=NAME_CHOICES, unique=True)
    max_collaborators = models.IntegerField(default=2)
    max_documents = models.IntegerField(default=5)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True)

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
