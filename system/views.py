from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages 
from system.models import MasterTable
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
from django.db import connections
def signup(request):
    if request.method == 'POST':
        USERNAME = request.POST.get('Name')
        name = request.POST.get('dir_name')
        email = request.POST.get('Email')
        password = request.POST.get('Password')
        address = request.POST.get('director_address')
        aadhar = request.POST.get('aadhar_card_number')
        licence_no = request.POST.get('director_licence_number')
        bank_name = request.POST.get('bank_name')
        mobile = request.POST.get('mobile_number')
        print(USERNAME,email,name,password,address,aadhar,licence_no,bank_name,mobile)
        if all([USERNAME, email, name, password, address, aadhar, licence_no, bank_name, mobile]):
            try:
                # Create user object and save to default database
                user = User.objects.create_user(username=USERNAME, email=email, password=password)
                # Save position as the first_name field
                user.first_name = name
                user.save()

                # Switch to the other database
                with connections['other_database'].cursor() as cursor:
                    cursor.execute(
    "INSERT INTO master_table (username, dir_name, password, email_id, mo_no, licence_no, aadhar, address, bank_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    [USERNAME, name, password, email, int(mobile), int(licence_no), int(aadhar), address, bank_name]
)


                success_message = 'User created successfully!'
                return render(request, 'signup.html', {'success_message': success_message})
            except Exception as e:
                error_message = f'An error occurred: {str(e)}'
                return render(request, 'signup.html', {'error_message': error_message})
        else:
            error_message = 'Incomplete form data. Please fill in all required fields.'
            return render(request, 'signup.html', {'error_message': error_message})

    # If form submission fails or it's a GET request, render the signup.html template
    return render(request, 'signup.html')


def empty_login_view(request):
    return render(request, 'login.html')

def regular_user_login(request):
    return render(request, 'login.html')

def home_view(request):
    # Get the username of the currently logged-in user
    user = request.user.username
    
    try:
        # Query the MasterTable model to get the record for the current user from the other database
        master_record = MasterTable.objects.using('other_database').get(username=user)
        bank_name = str(master_record.bank_name).upper()
        dir_name = str(master_record.dir_name).upper()

    except MasterTable.DoesNotExist:
        bank_name = None
        dir_name = None

    return render(request, 'home.html', {'name': bank_name, 'dir_name': dir_name})
