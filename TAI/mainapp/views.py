import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages  # Allows sending user-friendly messages
from django.http import JsonResponse
from .forms import SignUpForm, DocumentCreateForm
from .models import UserProfile, Document, Collaborator, User, Blacklist

from django.utils import timezone
from .forms import MessageForm, CustomAuthenticationForm
from .models import Message
from functools import wraps

# Create your views here.
# Home view (landing page)

def not_banned_required(function):
    """
    Decorator that checks if a user is banned and logs them out if they are.
    This decorator should be used in combination with login_required.
    """
    @wraps(function)
    def wrap(request, *args, **kwargs):
        user = request.user
        # Check if user has a userprofile and if they're banned
        try:
            # Access the profile through the OneToOneField relationship
            if user.userprofile.is_banned:
                # Log the user out
                logout(request)
                # Redirect to login page or a custom "banned" page
                return redirect('sign_in')  # Change to your login URL name
        except AttributeError:
            # Handle case where user might not have a profile
            pass
        
        return function(request, *args, **kwargs)
    return wrap

def login_not_banned_required(function):
    """
    Combined decorator that checks if user is both logged in and not banned.
    If user is banned, they will be logged out automatically.
    """
    return login_required(not_banned_required(function))

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

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'mainapp/sign_in.html'  # Adjust to your template path


@login_not_banned_required
def dashboard(request):
    # Get documents created by the user
    owned_documents = Document.objects.filter(user=request.user).order_by('-created_at')
    
    # Get documents the user is collaborating on
    collaborations = Collaborator.objects.filter(user=request.user).order_by('-added_at')
    
    context = {
        'owned_documents': owned_documents,
        'collaborations': collaborations,
    }
    
    return render(request, 'mainapp/dashboard.html', context)

# @login_not_banned_required
# def text_editor(request, pk = None):
#     if(pk == None):
#         return render(request, 'mainapp/text_editor.html')
#     else:
#         doc = get_object_or_404(Document, pk=pk, user=request.user)
#     return render(request, 'mainapp/text_editor.html', {
#         'document': doc
#         })

@login_not_banned_required
def text_editor(request, pk=None):
    if pk is None:
        doc = None
    else:
        doc = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'mainapp/text_editor.html', {'document': doc})


@login_not_banned_required
def user_settings(request):
    if request.method == 'POST':
        # Handle settings update
        return redirect('user-settings')
    return render(request, 'mainapp/user_settings.html')

'''
Creation post reques. DocumentCreateForm Is used to create the Docuement which will be created in the db
I had Gpt help me make this so idk why that else block is there (likley to call the form)
From my understanding, create_document is called when the new document page is loaded (GET), Then do stuff for POST
'''

@login_not_banned_required
def create_document(request):
    if request.method == 'POST':
        form = DocumentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            title   = form.cleaned_data['title']
            content = form.cleaned_data['content']
            uploaded = form.cleaned_data['file']
            
            # if they uploaded a .txt file, read it
            if uploaded:
                try:
                    content = uploaded.read().decode('utf-8')
                except UnicodeDecodeError:
                    content = uploaded.read().decode('latin-1')
            
            # finally save the Document
            doc = Document.objects.create(
                title=title,
                content=content,
                user=request.user
            )
            # redirect into the editor for this doc
            return redirect('text_editor', pk=doc.pk)
    else:
        form = DocumentCreateForm()
    
    return render(request, 'mainapp/create_document.html', {
        'form': form
    })

'''
Anthony
-added import json (line 1) to use since storeToDB used 'Content-Type': 'application/json',
-added save_document to save the text when editing after initial creation of text.
'''

@login_not_banned_required
def get_document(request, pk):
    print(f"get_document called: pk={pk}, user={request.user}, is_authenticated={request.user.is_authenticated}")
    if request.method != 'GET':
        print(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        doc = get_object_or_404(Document, pk=pk, user=request.user)
        return JsonResponse({
            'id': doc.pk,
            'title': doc.title,
            'content': doc.content,
            'created_at': doc.created_at.isoformat(),
            'latest_update': doc.latest_update.isoformat()
        })
    except Document.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)

@login_not_banned_required
def save_document(request, pk):
    if request.method == 'POST':
        try:
            doc = get_object_or_404(Document, pk=pk, user=request.user)
            data = json.loads(request.body)
            content = data.get('content')
            if content is not None:
                doc.content = content
                doc.save()
                return JsonResponse({
                    'message': 'Text saved successfully!',
                    'latest_update': doc.latest_update.isoformat()
                })
            return JsonResponse({'error': 'No content provided'}, status=400)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            raise  # Re-raise the exception to see the full traceback in the server logs
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# Inbox functionality
@login_not_banned_required
def inbox(request):
    # Get all messages for the current user
    received_messages = Message.objects.filter(recipient=request.user).order_by('-timestamp')
    sent_messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    
    # Get collaboration invites specifically for the "Invites" tab
    collaboration_invites = received_messages.filter(message_type=Message.MessageType.COLLABORATION)
    
    # Count unread messages and pending invites
    unread_count = received_messages.filter(is_read=False).count()
    pending_invites_count = collaboration_invites.filter(invitation_status=Message.InvitationStatus.PENDING).count()
    
    # Define data to be sent
    context = {
        'received_messages': received_messages,
        'sent_messages': sent_messages,
        'collaboration_invites': collaboration_invites,
        'unread_count': unread_count,
        'pending_invites_count': pending_invites_count,
        'form': MessageForm(),
    }
    return render(request, 'mainapp/inbox.html', context)

@login_not_banned_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is authorized to view this message
    if request.user != message.sender and request.user != message.recipient:
        messages.error(request, "You don't have permission to view this message.")
        return redirect('inbox')
    
    # Mark as read if recipient is viewing
    if request.user == message.recipient and not message.is_read:
        message.is_read = True
        message.read_timestamp = timezone.now()
        message.save()
    
    context = {
        'message': message,
        'reply_form': MessageForm(initial={'recipient': message.sender, 'subject': f"Re: {message.subject}"})
    }
    return render(request, 'mainapp/message_detail.html', context)

@login_not_banned_required
def send_message(request):
    # Get user's documents for collaboration invites
    user_documents = Document.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        message_type = request.POST.get('message_type', Message.MessageType.REGULAR)
        
        # For complaints, validate recipient is an admin
        if message_type == Message.MessageType.COMPLAINT:
            # Check how the recipient is being passed in the form
            recipient_value = request.POST.get('recipient')
            
            try:
                recipient = None
                try:
                    recipient = User.objects.get(username=recipient_value)
                except User.DoesNotExist:
                    try:
                        recipient = User.objects.get(id=recipient_value)
                    except (User.DoesNotExist, ValueError):
                        pass
                
                if not recipient:
                    messages.error(request, f"No user found with identifier: {recipient_value}")
                    form.add_error('recipient', "Recipient does not exist.")
                    return render(request, 'mainapp/send_message.html', {
                        'message_type': message_type,
                        'form': form,
                        'user_documents': user_documents
                    })
                
                # Check if recipient is admin for complaints
                if not recipient.is_staff:
                    form.add_error('recipient', "Please select an administrator.")
                    return render(request, 'mainapp/send_message.html', {
                        'message_type': message_type,
                        'form': form, 
                        'user_documents': user_documents
                    })
            except Exception as e:
                # Catch any other errors and log them
                print(f"Error validating recipient: {str(e)}")
                messages.error(request, f"Error validating recipient: {str(e)}")
                return render(request, 'mainapp/send_message.html', {
                    'message_type': message_type,
                    'form': form,
                    'user_documents': user_documents
                })
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.message_type = message_type
            
            # For collaboration invites
            if message_type == Message.MessageType.COLLABORATION:
                # (collaboration code unchanged)
                message.invitation_status = Message.InvitationStatus.PENDING
                document_id = request.POST.get('related_document')
                if document_id:
                    try:
                        document = Document.objects.get(id=document_id, user=request.user)
                        message.related_document = document
                    except Document.DoesNotExist:
                        messages.error(request, "Selected document does not exist or you don't have permission.")
                        return render(request, 'mainapp/send_message.html', {
                            'message_type': message_type,
                            'form': form,
                            'user_documents': user_documents
                        })
                else:
                    messages.error(request, "Please select a document to share.")
                    return render(request, 'mainapp/send_message.html', {
                        'message_type': message_type,
                        'form': form,
                        'user_documents': user_documents
                    })
            
            # Save the message
            message.save()
            return redirect('inbox')
        else:
            # Show detailed form errors
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            
            return render(request, 'mainapp/send_message.html', {
                'message_type': message_type,
                'form': form,
                'user_documents': user_documents
            })
    else:
        # For GET requests
        initial_data = {}
        
        # Check if complaint type is specified
        message_type = request.GET.get('type')
        
        # For complaints, pre-select an administrator
        if message_type and message_type.lower() == 'complaint':
            # Find an admin user
            admin_user = User.objects.filter(is_staff=True).first()
            if admin_user:
                print(f"Selected admin for complaint: {admin_user.username}")
                initial_data['recipient'] = admin_user
                initial_data['subject'] = "Complaint: "
        else:
            # For other messages
            recipient_id = request.GET.get('recipient')
            if recipient_id:
                try:
                    recipient = User.objects.get(id=recipient_id)
                    initial_data['recipient'] = recipient
                except User.DoesNotExist:
                    pass
        
        form = MessageForm(initial=initial_data)
    
    return render(request, 'mainapp/send_message.html', {
        'message_type': message_type,
        'form': form,
        'user_documents': user_documents
    })

@login_not_banned_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is authorized to delete this message
    if request.user != message.sender and request.user != message.recipient:
        messages.error(request, "You don't have permission to delete this message.")
        return redirect('inbox')
    
    message.delete()
    return redirect('inbox')

@login_not_banned_required
def get_unread_count(request):
    """API endpoint to get unread message count for the current user"""
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        return JsonResponse({'unread_count': unread_count})
    return JsonResponse({'unread_count': 0})

@login_not_banned_required
def handle_invitation(request, message_id, action):
    """Handle accepting or declining collaboration invitations"""
    invite = get_object_or_404(Message, id=message_id, message_type=Message.MessageType.COLLABORATION)
    
    # Verify the current user is the recipient of this invitation
    if request.user != invite.recipient:
        messages.error(request, "You don't have permission to respond to this invitation.")
        return redirect('inbox')
    
    # Check if invitation is still pending
    if invite.invitation_status != Message.InvitationStatus.PENDING:
        messages.error(request, f"This invitation has already been {invite.invitation_status.lower()}.")
        return redirect('inbox')
    
    # Update invitation status based on action
    if action == 'accept':
        invite.invitation_status = Message.InvitationStatus.ACCEPTED
        messages.success(request, "Collaboration invitation accepted!")
        
        # Add collaboration logic here
        if invite.related_document:
            try:
                # Create a new collaborator record
                Collaborator.objects.create(
                    document=invite.related_document,
                    user=request.user,
                    content=""  # Initialize with empty content or default text
                )
            except Exception as e:
                # Log the error but don't interrupt the process
                print(f"Error adding collaborator: {e}")
                
    elif action == 'decline':
        invite.invitation_status = Message.InvitationStatus.DECLINED
        messages.success(request, "Collaboration invitation declined.")
    else:
        messages.error(request, "Invalid action specified.")
        return redirect('inbox')
    
    # Save the updated invitation
    invite.save()
    
    return redirect('inbox')