from django.db import models

# Create your models here.

class Accounts(models.Model):
    username = models.CharField(max_length=150, unique=True, primary_key= True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    LEVEL_CHOICES = [
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('admin', 'Admin'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default='free')
    tokens = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Payment(models.Model):
    owner = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='payments')
    payment_method_data = models.TextField()
    payment_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Payment {self.payment_id} by {self.owner.username}"

class Mailbox(models.Model):
    owner = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='mailboxes')
    message = models.TextField()
    invite_link = models.URLField()
    mail_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Mailbox {self.mail_id} for {self.owner.username}"

class Doc(models.Model):
    owner = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='documents')
    doc_id = models.CharField(max_length=100, unique=True)
    text_data = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    tokens_used = models.IntegerField(default=0)

    def __str__(self):
        return f"Document {self.doc_id} owned by {self.owner.username}"

class Collaborator(models.Model):
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='collaborations')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='collaborators')
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} collaborates on {self.doc.doc_id}"

class Complaint(models.Model):
    owner = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='complaints_made')
    admin = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name='complaints_handled')
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='complaints')
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint on {self.doc.doc_id} by {self.owner.username}"

class Blacklist(models.Model):
    doc = models.ForeignKey(Doc, on_delete=models.CASCADE, related_name='blacklists')
    banned_word = models.CharField(max_length=255)
    blacklist_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Banned Word '{self.banned_word}' for Doc {self.doc.doc_id}"
