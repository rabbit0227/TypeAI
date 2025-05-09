import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages
from django.http import JsonResponse
from .forms import SignUpForm, DocumentCreateForm
from .models import UserProfile, Document


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

# experiance section
@login_required
def dashboard(request):
    users_documents = Document.objects.filter(user=request.user)
    return render(request, 'mainapp/dashboard.html', { 'documents' : users_documents})

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
        return redirect('settings')
    return render(request, 'mainapp/settings.html')

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