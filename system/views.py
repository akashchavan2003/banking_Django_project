from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            print("logined....")
            return redirect('home')  # Redirect to home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def superuser_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('super_username')
        password = request.POST.get('super_password')
        superuser = authenticate(request, username=username, password=password)
        if superuser is not None and superuser.is_superuser:
            login(request, superuser)
            return redirect('signup')  # Redirect to signup after successful superuser login
        else:
            messages.error(request, 'Invalid superuser username or password')
    return render(request, 'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST.get('name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        password = request.POST.get('password')
        confirm_data = request.POST.get('data')

        # Check if all required fields are provided
        if username and email and position and password:
            # Create user object and save to database
            user = User.objects.create_user(username=username, email=email, password=password)
            # Save position as a custom field (you can use 'first_name' for this purpose)
            user.first_name = position
            user.save()
            # Render the signup.html template with a success message
            return render(request, 'signup.html', {'success_message': 'User created successfully!'})
    
    # If form submission fails or it's a GET request, prints the fails msg
    print("fails..")
    return render(request, 'signup.html')
    



def empty_login_view(request):
    return render(request, 'login.html')

def regular_user_login(request):
    return render(request, 'login.html')
def home_view(request):
    return render(request,'home.html')