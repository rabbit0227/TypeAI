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

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'mainapp/sign_in.html'  # Adjust to your template path
    

@login_required
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

# @login_required
# def text_editor(request, pk = None):
#     if(pk == None):
#         return render(request, 'mainapp/text_editor.html')
#     else:
#         doc = get_object_or_404(Document, pk=pk, user=request.user)
#     return render(request, 'mainapp/text_editor.html', {
#         'document': doc
#         })

@login_required
def text_editor(request, pk=None):
    if pk is None:
        doc = None
    else:
        doc = get_object_or_404(Document, pk=pk, user=request.user)
    return render(request, 'mainapp/text_editor.html', {'document': doc})


@login_required
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

@login_required
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

@login_required
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

@login_required
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
@login_required
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

@login_required
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

@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        message_type = request.POST.get('message_type', Message.MessageType.REGULAR)
        
        # For complaints, validate recipient is an admin
        if message_type == Message.MessageType.COMPLAINT:
            recipient_username = request.POST.get('recipient')
            try:
                recipient = User.objects.get(username=recipient_username)
                if not recipient.is_staff:
                    messages.error(request, "Complaints can only be sent to administrators.")
                    form.add_error('recipient', "Please select an administrator.")
                    return render(request, 'mainapp/send_message.html', {'form': form})
            except User.DoesNotExist:
                messages.error(request, "Selected recipient does not exist.")
                return render(request, 'mainapp/send_message.html', {'form': form})
        
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.message_type = message_type
            
            # For collaboration invites, set initial status and link document
            if message_type == Message.MessageType.COLLABORATION:
                message.invitation_status = Message.InvitationStatus.PENDING
                document_id = request.POST.get('related_document')
                if document_id:
                    try:
                        document = Document.objects.get(id=document_id, user=request.user)
                        message.related_document = document
                    except Document.DoesNotExist:
                        messages.error(request, "Selected document does not exist or you don't have permission.")
                        return render(request, 'mainapp/send_message.html', {'form': form})
                else:
                    messages.error(request, "Please select a document to share.")
                    return render(request, 'mainapp/send_message.html', {'form': form})
            
            message.save()
            messages.success(request, f"{message_type} sent successfully!")
            return redirect('inbox')
        else:
            messages.error(request, "Error sending message. Please check the form.")
    else:
        # For GET requests, prefill recipient if provided in URL
        recipient_id = request.GET.get('recipient')
        initial_data = {}
        if recipient_id:
            try:
                recipient = User.objects.get(id=recipient_id)
                initial_data['recipient'] = recipient
            except User.DoesNotExist:
                pass
        form = MessageForm(initial=initial_data)
    
    # Get user's documents for collaboration invites
    user_documents = Document.objects.filter(user=request.user)
    
    return render(request, 'mainapp/send_message.html', {
        'form': form,
        'user_documents': user_documents
    })

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

@login_required
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