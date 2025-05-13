from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Allows sending user-friendly messages
from django.db import transaction
from .forms import SignUpForm, BankInfoForm
from .models import UserProfile, Card, TokensPackage, Transaction

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
    return render(request, 'mainapp/text_editor.html', {'user_profile' : request.user.userprofile})

@login_required
def user_settings(request):
    if request.method == 'POST':
        # Handle settings update
        return redirect('user-settings')
    return render(request, 'mainapp/user_settings.html')

@login_required
def tokens(request):
    packages = TokensPackage.objects.all()
    return render(request, 'mainapp/tokens.html', {'packages' : packages, 'user_profile' : request.user.userprofile})

@login_required
def select_package(request, package_id):
    request.session['selected_package_id'] = package_id
    return redirect('tokens_landing')

@login_required
def upgrade_user(request):
    user = request.user.userprofile
    if user.tier != 'Free':
        messages.info(request, "You are already a paid user")
        return redirect('tokens_landing')
    
    # The user should not have a card in the DB if they're upgrading (one time purchase)
    # But, in the case we decide to swap to a subscription model, this is here for that
    # try:
    #     card_info = Card.objects.get(user=user.associated_user)
    # except Card.DoesNotExist:
    # place card_info under this if we decide to do multiple cards
    card_info = None
    
    if request.method == "POST":
        form = BankInfoForm(request.POST)

        if form.is_valid():
            # save card info
            if card_info is None:
                card_info = form.save(commit=False)
                card_info.user = user.associated_user
                card_info.save()

            with transaction.atomic():
                # transaction to paid user, checking if acc is valid with $1 charge
                Transaction.objects.create(
                    user=user.associated_user,
                    package="upgrade",
                    price=1.00,
                    card=card_info
                )
            
            user.tier = "Paid"
            user.save()
            
            messages.success(request, "You are now a PAID user!")
            redirect('text_editor')
    else:
        form = BankInfoForm()

    return render(request, 'mainapp/upgrade.html', {'form' : form, 'card_info' : card_info})
@login_required
def cart(request):
    user = request.user.userprofile

    if user.tier != "Paid" and user.tier != "Super":
        messages.error(request, "You must be a PAID user to purchase tokens.")
        return redirect('upgrade_user')
    
    package_id = request.session.get('selected_package_id')

    if not package_id:
        messages.error(request, "No package selected. Please select a package first.")
        return redirect('tokens_landing')
    
    try:
        # Get the selected package from the db
        package = TokensPackage.objects.get(id=package_id)
    except TokensPackage.DoesNotExist:
        # If the package dne for w/e reason
        messages.error(request, "Selected packaged DNE.")
        return redirect('tokens_landing')
    
    # Get paid user associated card
    cards = Card.objects.filter(user=user.associated_user).first()
    
    if request.method == 'POST':
        # commented code for multiple card options
        # selected_card_id = request.POST.get('card_id')

        # if not selected_card_id:
        #     messages.error(request, "Please selected a payment method.")
        #     return redirect('payment_cart')
        
        # try:
        #     # get card from db
        #     selected_card = Card.objects.get(id=selected_card_id, user=user.associated_user)
        # except Card.DoesNotExist:
        #     messages.error(request, "Invalid payment method.")
        #     return redirect('payment_cart')

    # since this is simulated we only have success on transaction
        with transaction.atomic():
            Transaction.objects.create(
                user=user.associated_user,
                package=package.name,
                price=package.price,
                card=cards
            ) # card=selected_card for the case of allowing more than 1 card in db

            user.tokens += package.token_value
            user.save()

        request.session.pop('selected_package_id', None)

        return redirect('tokens_landing') # Make a thank you page to redirect to.

    return render(request, 'mainapp/cart.html', {'package' : package, 'cards' : cards, 'user_profile' : request.user.userprofile})


"""function to load """