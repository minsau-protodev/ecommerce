from accounts.models import Account
from django.shortcuts import render
from .forms import RegistrationForm
from time import time

# Create your views here.

# Register a new user
def register(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            # confirm_password = form.cleaned_data['confirm_password']

            username = f"{email.split('@')[0]}_{time()}"

            user = Account.objects.create_user(
                first_name=first_name, 
                last_name=last_name,
                email=email,
                password=password,
                username=username
            )
    
            user.phone_number = phone_number
            user.save()
    else:
        form = RegistrationForm()
    
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context=context)

#Login a user
def login(request):
    return render(request, 'accounts/login.html')

#logout a user
def logout(request):
    pass