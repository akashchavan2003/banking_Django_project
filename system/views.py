from itertools import count
from modulefinder import packagePathMap
import re
import sqlite3
from time import process_time_ns
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages 
import system
import system.bank_managament_system
from system.models import MasterTable,CashInHand,PersonalBankAccount
from system import bank_managament_system
from django.http import HttpResponse
from system.bank_managament_system import Account, get_current_date
from django.contrib.auth.decorators import login_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login_username')
        password = request.POST.get('login_password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            print("logined....")
            messages.error(request, 'Invalid username or password')
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
@login_required
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
        count = PersonalBankAccount.objects.using('other_database').filter(username=user).count()
        reg=str(master_record.licence_no)
        dt=get_current_date()
# Get the count of occurrences of the username in the table
    except MasterTable.DoesNotExist:
        bank_name = None
        dir_name = None
        cash_in_hand=0
    return render(request, 'home.html', {'name': bank_name, 'dir_name': dir_name,'cash_hand':cash_in_hand,'account_count':count,'reg_no':"REG NO."+reg,'date':dt})


def check_ac_bal(request):
    customer = None
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        try:
            customer = PersonalBankAccount.objects.using('other_database').get(account_number=account_number)
            if customer:
                print(customer.account_holder_name)
                return render(request, 'check_ac_bal.html', {'customer': customer})
        except PersonalBankAccount.DoesNotExist:
            em="Ac number Not Found Please Try Again...!"
            return render(request,'check_ac_bal.html',{'msg':em})
        except Exception as e:
            print("Error happend at the check_ac_bal",e)
    return render(request,'check_ac_bal.html')
@login_required
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
                        chk=a1.Deposit()

                    except Exception as e :
                        print("error occured in deposit function ",e)   
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

@login_required
def debit(request):
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
                        chk=a1.withdraw()

                    except Exception as e :
                        print("error occured in deposit function ",e)   
                else:
                    return HttpResponse("Account not found")
            except Exception as e:
                return HttpResponse("Deposit failed",e)
   if 'check_button' in request.POST:
            print("Button check clicked")
            ac_no = request.POST.get('account_number')
            if bank_managament_system.ac_availability(ac_no):
                try:
                    with connections['other_database'].cursor() as cursor:
                        cursor.execute("SELECT account_holder_name, balance FROM personal_bank_account WHERE account_number = %s", [ac_no])
                        row = cursor.fetchone()
                        if row:
                            ac_name, ac_bal = row
                            return render(request, 'debit.html', {'account_holder_name': ac_name, 'account_balance': ac_bal})
                        else:
                            return HttpResponse("No account found with the provided account number.")
                except Exception as e:
                    # Handle database query or other errors
                    print("Error:", e)
                    return HttpResponse("Error occurred while fetching account holder name.")
            else:
                print("Account not found")
                return HttpResponse("Account not found.")
   return render(request,'debit.html')

def trf(request):
    user = request.user.username
    print("creating object of personal bank account")
    accounts = PersonalBankAccount.objects.using('other_database').filter(username=user)
    print("initalizing the data")
    initial_data = {f'{account.account_number}-{account.account_holder_name}': f'{account.account_number}-{account.account_holder_name}' for account in accounts}

    context = {
        'initial_data': initial_data,
    }
    print("makin attributes of classes in forms.py")
    


    if request.method == 'POST':
            fa =request.POST.get("from_account")
            ta = request.POST.get("to_account")
            fa1=str(fa).split("-")
            ta1=str(ta).split("-")
            from_account=int(fa1[0])
            to_account=int(ta1[0])
            print(from_account)
            print(fa[0])
            if from_account==to_account:
                msg="Same Account Number is Not Valid..."
                return render(request,'trf.html',{'msg':msg})
            else:
            # Processing the transfer here
                amt = request.POST.get('amount')
                customer1 = PersonalBankAccount.objects.using('other_database').get(account_number=from_account)
                payee_ac_bal=int(customer1.balance)
                a1 = Account(amt6=amt, user=user, an2=0)
                try:
                        chk = a1.transfer(from_account, to_account)
                        if chk==True:
                            # Get the updated account details
                            customer1 = PersonalBankAccount.objects.using('other_database').get(account_number=from_account)
                            customer2 = PersonalBankAccount.objects.using('other_database').get(account_number=to_account)
                            msg = f"Amt: {amt} is successfully Transferred From {from_account} To {to_account}"
                            return render(request, 'trf.html', {
                                'suc_msg': msg,
                                'from_account_number': from_account,
                                'from_account_holder_name': customer1.account_holder_name,
                                'from_account_balance': customer1.balance,
                                'to_account_number': to_account,
                                'to_account_holder_name': customer2.account_holder_name,
                                'to_account_balance': customer2.balance
                            })
                        if chk=="balance low":
                            msg1="Transfer Failed...Due To Low balance In AC No:"+str(from_account)
                            return render(request,'trf.html',{'msg':msg1})
                        else:
                            msg3="Transfer Failed....."
                            return render(request,'trf.html',{'msg':msg3})
                except sqlite3.DatabaseError as e:
                    print("from views",e)
                except Exception as e :
                        print("from views",e)
                        return render(request,'trf.html',{'msg':e})
               
    return render(request, 'trf.html',context)
def create_account(request):
    user = request.user.username
    if request.method == 'POST':
        nm = request.POST.get('account_holder_name')
        at = request.POST.get('account_type')
        ad = request.POST.get('address')
        mn = request.POST.get('mobile_number')
        an = request.POST.get('aadhar_card_number')
        pn = request.POST.get('pan_card_number')
        if all([nm,at,ad,mn,an,pn,user]):
            try:
                ac_no=system.bank_managament_system.create_ac(nm,at,ad,mn,an,pn,user)
                print(ac_no)
                msg="Account Created Sucessfully With Account Number:"+str(ac_no)
                return render(request,'create_account.html',{'msg':msg})
            except Exception as e:
                msg2="Error Occured During Creating Account"
                return render(request,'create_account.html',{'msg2':msg2})
    return render(request,'create_account.html')
