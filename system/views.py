from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages 
from system.models import MasterTable,CashInHand
from system import bank_managament_system
from django.http import HttpResponse
from django.http import JsonResponse
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
    cash_in_hand=0
    try:
        # Query the MasterTable model to get the record for the current user from the other database
        master_record = MasterTable.objects.using('other_database').get(username=user)
        bank_name = str(master_record.bank_name).upper()
        dir_name = str(master_record.dir_name).upper()
       
        cash_in_hand_instance = CashInHand.objects.using('other_database').get(username=user)
        cash_in_hand = int(cash_in_hand_instance.cash_in_hand)

    except MasterTable.DoesNotExist:
        bank_name = None
        dir_name = None
        cash_in_hand=0
    return render(request, 'home.html', {'name': bank_name, 'dir_name': dir_name,'cash_hand':cash_in_hand})


def check_ac_bal(request):
    return render(request,'check_ac_bal.html')
def credit(request):
    user = request.user.username
    if 'submit_button' in request.POST:
            ac_no=request.POST.get("account_number0")
            amt=request.POST.get("amount")
            print(ac_no,amt)
            try:
                #Checking account avilability
                if bank_managament_system.ac_availability(ac_no):
                    a1=bank_managament_system.Account(ac_no,amt,user)
                    try:
                        chk=a1.deposit()
                        print(chk[0],chk[1])
                        if chk[0]:
                            try:
                            # getting cash in hand details by orm
                                print("getting cash in hand ")
                                cash_in_hand_instance = CashInHand.objects.using('other_database').get(username=user)
                                cash_in_hand = (cash_in_hand_instance.cash_in_hand)
                                print(cash_in_hand)
                            except:
                                print("error while getting cash in hand info")
                                return HttpResponse("Error while getting cash in hand info")
                            #adding cash in hand + amt to set or update
                            set_amt=int(cash_in_hand)+int(amt)
                            print(set_amt)
                            try:
                                print("creating objct of wallet class")
                                w1=bank_managament_system.Wallet(set_amt=set_amt,user=user,cih=cash_in_hand)
                                print("calling cash in deposit")
                                v=w1.cash_in_hand_deposit()
                                print(v)
                                if v:
                                  print("amt deposited")
                            except Exception as e:
                                return HttpResponse("error in adding cash in hand operations",e)
                        else:
                            print("normal deposit not works")
                    except Exception as e :
                        print("error occured ",e)   
                else:
                    return HttpResponse("Account not found")
            except Exception as e:
                return HttpResponse("Deposit failed",e)
    if 'check_button' in request.POST:
            print("Button check clicked")
            ac_no = request.POST.get('account_number')
            print(ac_no)
            if bank_managament_system.ac_availability(ac_no):
                try:
                    with connections['other_database'].cursor() as cursor:
                        cursor.execute("SELECT account_holder_name, balance FROM personal_bank_account WHERE account_number = %s", [ac_no])
                        row = cursor.fetchone()
                        if row:
                            ac_name, ac_bal = row
                            return render(request, 'credit.html', {'account_holder_name': ac_name, 'account_balance': ac_bal})
                        else:
                            return HttpResponse("No account found with the provided account number.")
                except Exception as e:
                    # Handle database query or other errors
                    print("Error:", e)
                    return HttpResponse("Error occurred while fetching account holder name.")
            else:
                print("Account not found")
                return HttpResponse("Account not found.")
    return render(request, 'credit.html')


def debit(request):
   return render(request,'debit.html')

def trf(request):
   return render(request,'trf.html')