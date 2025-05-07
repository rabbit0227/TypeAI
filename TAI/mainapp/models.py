from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # for message date
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
        return f"{self.associated_user.username}'s profile"
# }

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# might split this into complaints and collab invites
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.subject} - From: {self.sender.username} To: {self.recipient.username}"
    
    class Meta:
        ordering = ['-timestamp']