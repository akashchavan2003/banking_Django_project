from ast import Pass
from itertools import count
from modulefinder import packagePathMap
import re
import sqlite3
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from markupsafe import EscapeFormatter 
import system
import system.bank_managament_system
from system.models import FDAccountModel, MasterTable,CashInHand,PersonalBankAccount,RDAccountModel
from system import bank_managament_system
from django.http import HttpResponse
from system.bank_managament_system import Account, Fdaccount, RDaccount, get_current_date
from django.contrib.auth.decorators import login_required

import system.models
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

def fd_account(request):
    if request.method == 'POST':
        print("FIrst form")
        if 'submitForm1' in request.POST:
            # Process the submission of the first form to obtain account information
            try:
                ac_no = request.POST.get('from_account').split('-')[0]
                customer = PersonalBankAccount.objects.using('other_database').get(account_number=int(ac_no))
                return render(request, 'fd_account.html', {'customer': customer,'ac_no':ac_no})
            except PersonalBankAccount.DoesNotExist:
                error_message = "Personal Bank Account not found."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
            return render(request, 'fd_account.html', {'error_message': error_message})

        elif 'submitForm2' in request.POST:
            print("in second form")
            # Process the submission of the second form to open an FD account
            try:
               
                ac_no = request.POST.get('ac_no', '')
                fd_amount = request.POST.get('deposit_amount')
                fd_duration = request.POST.get('duration')
                int_rate = request.POST.get('interest_rate')

                # Validate form data
                if fd_amount and fd_duration and int_rate and ac_no:
                    print("form validated")
                    # Assuming create_account method returns True on success
                    f1=Fdaccount()
                    bol = f1.create_account(request.user.username, ac_no, fd_amount, fd_duration, int_rate)
                    if bol:
                        last_account = FDAccountModel.objects.using('other_database').order_by('-id').first()
                        print("function excuted......")
                        return render(request, 'fd_account.html', {'error_message': "Account Created Successfully With Ac.No:"+last_account.fd_ac_no})
                    else:
                        error_message = "Account Creation Failed."
                else:
                    error_message = "All fields are required."
            except Exception as e:
                error_message = f"An error occurred from the second form: {str(e)}"
            return render(request, 'fd_account.html', {'error_message': error_message})
    else:
        # Render the initial page with the first form
        user1 = request.user.username
        accounts = PersonalBankAccount.objects.using('other_database').filter(username=user1)
        initial_data = {f'{account.account_number}-{account.account_holder_name}': f'{account.account_number}-{account.account_holder_name}' for account in accounts}
        context = {'initial_data': initial_data}
        return render(request, 'fd_account.html', context) 
    
def rd_account(request):
    if request.method == 'POST':
        print("FIrst form")
        if 'submitForm1' in request.POST:
            # Process the submission of the first form to obtain account information
            try:
                ac_no = request.POST.get('from_account').split('-')[0]
                customer = PersonalBankAccount.objects.using('other_database').get(account_number=int(ac_no))
                return render(request, 'rd_account.html', {'customer': customer,'ac_no':ac_no})
            except PersonalBankAccount.DoesNotExist:
                error_message = "Personal Bank Account not found."
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
            return render(request, 'rd_account.html', {'error_message': error_message})

        elif 'submitForm2' in request.POST:
            print("in second form")
            # Process the submission of the second form to open an FD account
            try:
               
                ac_no = request.POST.get('ac_no', '')
                fd_amount = request.POST.get('deposit_amount')
                fd_duration = request.POST.get('duration')
                int_rate = request.POST.get('interest_rate')

                # Validate form data
                if fd_amount and fd_duration and int_rate and ac_no:
                    print("form validated")
                    # Assuming create_account method returns True on success
                    f1=RDaccount()
                    bol = f1.create_rd_account(request.user.username, ac_no, fd_amount, fd_duration, int_rate)
                    if bol:      
                        last_account = RDAccountModel.objects.using('other_database').order_by('-id').first()
                        print("function excuted......")
                        return render(request, 'rd_account.html', {'error_message': "Account Created Successfully With Ac.No:"+ last_account.rd_ac_no})
                    else:
                        error_message = "Account Creation Failed."
                else:
                    error_message = "All fields are required."
            except Exception as e:
                error_message = f"An error occurred from the second form: {str(e)}"
            return render(request, 'rd_account.html', {'error_message': error_message})
    else:
        # Render the initial page with the first form
        user1 = request.user.username
        accounts = PersonalBankAccount.objects.using('other_database').filter(username=user1)
        initial_data = {f'{account.account_number}-{account.account_holder_name}': f'{account.account_number}-{account.account_holder_name}' for account in accounts}
        context = {'initial_data': initial_data}
        return render(request, 'rd_account.html', context)

def gold_loan(request):
    pass


def fund_rd_ac(request):
    return render(request,'fund_rd.html')

from django.db import transaction

@login_required
def fund_fd_ac(request):
    user1 = request.user.username
    global ac_no

    if request.method == 'POST':
        # this is for specially for first dropdown to show all fd accounts to the user with the button
        if 'submitForm1' in request.POST:
            ac_no = request.POST.get('from_account').split('-')[0]
            try:
                fdobj = FDAccountModel.objects.using('other_database').get(fd_ac_no=ac_no)
                return render(request, 'fund_fd.html', {'fdobj': fdobj, 'FD': True, 'selected_account': ac_no})
            except FDAccountModel.DoesNotExist:
                return render(request, 'fund_fd.html', {'error': 'FD account does not exist.', 'selected_account': ac_no})
        # this is second button where the user selects the transfer type 
        elif 'submitForm2' in request.POST:
            transfer_type = request.POST.get('transferType')
            try:
                info = FDAccountModel.objects.using('other_database').get(fd_ac_no=int(ac_no))
                
                if info.account_balance == info.fd_opening_amt:
                    return render(request, 'fund_fd.html', {'error': "This Account is Already Funded...", 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                # if user cash selects cash the they calls class and object
                if transfer_type == 'cash':
                    print("in cash")
                    if 'cash_proceed' in request.POST:
                        print("in the POST method")
                        if request.POST.get('cash_proceed') == 'save':
                            print("in save")
                            try:
                                obj = Fdaccount()
                                chk = obj.add_funds(fd_obj=info, user=user1, ac_no=ac_no)
                                if chk:
                                    return render(request, 'fund_fd.html', {'success': 'Cash Added Successfully To FD Account.', 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                                else:
                                    return render(request, 'fund_fd.html', {'error': "Error To deposit Cash", 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                            except Exception as e:
                                print(e)
                                return render(request, 'fund_fd.html', {'error': str(e), 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                        else:
                            print("pressed cancel")
                            return redirect('fund_fd')
                    else:
                        print("entered in the else")
                        return render(request, 'fund_fd.html', {'cash': True, 'FD': True, 'fdobj': info, 'selected_account': ac_no, 'Proceed': True})
 
                        
                # means the user selects the transfer type from saving and now here we check the account balance 
                # if the account balnce is greater or equal then we reneder the blance where we show the buttons to proceed
                # if balance meets then we show the msg 
                else:
                    try:
                        account = PersonalBankAccount.objects.using('other_database').get(username=user1, account_number=info.personal_ac_no)
                        if account.balance >= info.fd_opening_amt:
                            return render(request, 'fund_fd.html', {'account': account, 'balance': True, 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                        else:
                            return render(request, 'fund_fd.html', {'error': 'Insufficient balance in savings account.', 'account': account, 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                    except Exception as e:
                        print(e)
                    return render(request, 'fund_fd.html', {'FD': True, 'fdobj': info, 'selected_account': ac_no})
            except Exception as e:
                print("Problem in the second button", e)
                return render(request, 'fund_fd.html', {'FD': True, 'selected_account': ac_no})
        # it works when upper returns and renders the balance account and FD and if the balance is less then this blocks skips
        # because the condition not meets it means the else blocks firstly renders the buttons that why elif condition meets for POST method 
        # if they did not meet the elif conditions it means the account balance is lower
        elif 'action' in request.POST:
            action = request.POST.get('action')
            try:
                info = FDAccountModel.objects.using('other_database').get(fd_ac_no=int(ac_no))
                account = PersonalBankAccount.objects.using('other_database').get(username=user1, account_number=info.personal_ac_no)
                
                if action == 'save':
                    print("Proceed button pressed")
                    with transaction.atomic(using='other_database'):
                        if account.balance >= info.fd_opening_amt:
                            account.balance -= info.fd_opening_amt
                            account.save()
                            info.account_balance = info.fd_opening_amt
                            info.save()
                            return render(request, 'fund_fd.html', {'success': 'Funds transferred successfully.', 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                        else:
                            return render(request, 'fund_fd.html', {'error': 'Insufficient balance in savings account.', 'account': account, 'FD': True, 'fdobj': info, 'selected_account': ac_no})
                
                elif action == 'delete':
                    print("Cancel button pressed")
                    return redirect('fund_fd')  # Replace 'fund_fd_ac' with the appropriate URL name for the fund_fd_ac view
            
            except Exception as e:
                print(e)
                return render(request, 'fund_fd.html', {'error': 'Error while processing the action.', 'FD': True, 'fdobj': info, 'selected_account': ac_no})

    else:
        accounts = FDAccountModel.objects.using('other_database').filter(username=user1)
        initial_data = {f'{account.fd_ac_no}-{account.customer_name}': f'{account.fd_ac_no}-{account.customer_name}' for account in accounts}
        context = {'initial_data': initial_data}
        return render(request, 'fund_fd.html', context)
    

def fd_loan(request):
    user1=request.user.username
    if request.method == 'POST':
        # this is for specially for first dropdown to show all fd accounts to the user with the button
        if 'submitForm1' in request.POST:
            ac_no = request.POST.get('from_account').split('-')[0]
            try:
                info = FDAccountModel.objects.using('other_database').get(fd_ac_no=ac_no)
                return render(request, 'fd_loan.html',{'info':info,'FDTrue':True})
            except FDAccountModel.DoesNotExist:
                return render(request, 'fund_fd.html', {'error': 'FD account does not exist.', 'selected_account': ac_no})
        # this is second button where the user selects the
      
        elif 'detailsForm' in request.POST:
                LIMIT=1000
                amount = float(request.POST.get('amount', 0))
                interest_rate = float(request.POST.get('interest_rate', 0))
                months = int(request.POST.get('months', 0))
                return render(request, 'details_form.html',{'limit':LIMIT})
        return render(request, 'details_form.html',{'limit':LIMIT})
    
    else:
        accounts = FDAccountModel.objects.using('other_database').filter(username=user1)
        initial_data = {f'{account.fd_ac_no}-{account.customer_name}': f'{account.fd_ac_no}-{account.customer_name}' for account in accounts}
        context = {'initial_data': initial_data}
        return render(request, 'fd_loan.html', context)
    
