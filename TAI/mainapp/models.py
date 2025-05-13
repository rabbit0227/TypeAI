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
    
    is_banned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.associated_user.username}'s profile"
# }

class Document(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    latest_update = models.DateTimeField(auto_now=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (f"ID: {self.id}\n TITLE: {self.title}\n CONTENT: Didnt paste here for sanity\n CREATION: {self.created_at}\n LATEST: {self.latest_update}\n USERID: {self.user}")

# might split this into complaints and collab invites
class Message(models.Model):
    class MessageType(models.TextChoices):
        REGULAR = 'Regular', 'Regular Message'
        COLLABORATION = 'Collaboration', 'Collaboration Invite'
        COMPLAINT = 'Complaint', 'Admin Complaint'
    
    class InvitationStatus(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ACCEPTED = 'Accepted', 'Accepted'
        DECLINED = 'Declined', 'Declined'
    
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_timestamp = models.DateTimeField(null=True, blank=True)
    
    # New fields for message categorization
    message_type = models.CharField(
        max_length=15,
        choices=MessageType.choices,
        default=MessageType.REGULAR
    )
    
    # Fields specific to collaboration invites
    invitation_status = models.CharField(
        max_length=10,
        choices=InvitationStatus.choices,
        null=True,
        blank=True
    )
    
    # For references to related objects (like documents for collaboration)
    related_document = models.ForeignKey(
        Document, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_invites'
    )
    
    def __str__(self):
        return f"{self.subject} - From: {self.sender.username} To: {self.recipient.username}"
    
    class Meta:
        ordering = ['-timestamp']


class Blacklist(models.Model):
    word = models.CharField(max_length=100, unique=True)  # max_length can be modified, 
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='requested_blacklist_words')
    # black listed words shouldn't be deleted when a user deletes
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.word} (requested by {self.requested_by.username if self.requested_by else 'Unknown'})"
    
    class Meta:
        ordering = ['word']
        
class Collaborator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    # this will contain the all the documents a user is collaborating in
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='collaborators')
    # this will get all the users that are collaborating on a document
    added_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    
def __str__(self):
        return f"{self.user.username} - {self.document.title}"