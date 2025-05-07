from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages
from django.http import JsonResponse
from django.utils import timezone
from .forms import SignUpForm, MessageForm
from .models import UserProfile, Message

# Create your views here.
# Home view (landing page)
def home_page(request):
    return render(request, 'mainapp/home.html')

# user section
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign_in')
    else:
        form = SignUpForm()
    return render(request, 'mainapp/sign_up.html', {'form': form})

# experience section
@login_required
def dashboard(request):
    return render(request, 'mainapp/dashboard.html')

@login_required
def text_editor(request):
    return render(request, 'mainapp/text_editor.html')

@login_required
def user_settings(request):
    if request.method == 'POST':
        # Handle settings update
        return redirect('user-settings')
    return render(request, 'mainapp/user_settings.html')

# Inbox functionality
@login_required
def inbox(request):
    # Get all messages for the current user
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
    # Count unread messages, this will be sent to another view
    unread_count = received_messages.filter(is_read=False).count()
    
    #define data to be sent
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'unread_count': unread_count,
        'form': MessageForm(),
    }
    return render(request, 'mainapp/inbox.html', context)

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is authorized to view this message
    # should never happen tho
    if request.user != message.sender and request.user != message.recipient:
        messages.error(request, "You don't have permission to view this message.")
        return redirect('inbox')
    
    # Mark as read if recipient is viewing
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        # the read time is wrong, idk if browser is wrong or its reading wrong
        # fix or remove later
        message.read_timestamp = timezone.now()
        message.save()
    
    context = {
        'message': message,
        'reply_form': MessageForm(initial={'recipient': message.sender, 'subject': f"Re: {message.subject}"})
    }
    return render(request, 'mainapp/message_detail.html', context)

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            messages.success(request, "Message sent successfully!")
            return redirect('inbox')
        else:
            messages.error(request, "Error sending message. Please check the form.")
    else:
        form = MessageForm()
    
    return render(request, 'mainapp/send_message.html', {'form': form})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is authorized to delete this message
    if request.user != message.sender and request.user != message.recipient:
        messages.error(request, "You don't have permission to delete this message.")
        return redirect('inbox')
    
    message.delete()
    messages.success(request, "Message deleted successfully!")
    return redirect('inbox')

@login_required
def get_unread_count(request):
    """API endpoint to get unread message count for the current user"""
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})