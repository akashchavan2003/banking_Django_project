from django.db import models
from django.core.validators import MinValueValidator

class CashInHand(models.Model):
    username = models.CharField(max_length=50,primary_key=True,unique=True)
    cash_in_hand = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'cash_in_hand'
    def __str__(self):
        return self.username,self.cash_in_hand
        

class CashTransaction(models.Model):
    ac_no = models.IntegerField()
    transaction_type = models.CharField(max_length=255)
    date = models.CharField(max_length=255)
    amt = models.IntegerField()
    cash_in_hand_previous = models.CharField(max_length=255,default='N')
    voucher_no = models.IntegerField()
    frm_ac_no = models.IntegerField()
    to_ac_no = models.IntegerField()
    username = models.CharField(max_length=50, primary_key=True)
    narration = models.TextField(default="")

    class Meta:
        db_table = 'cash_transaction'
    def __str__(self):
        return self.ac_no
        

class DeletedAccount(models.Model):
    account_number = models.AutoField(primary_key=True)
    account_holder_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    account_type = models.CharField(max_length=20)
    opening_date = models.DateField()
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    aadhar_card_number = models.CharField(max_length=20)
    pan_card_number = models.CharField(max_length=20)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = 'deleted_ac'
    def __str__(self):
        return self.account_holder_name
        

        

class PersonalBankAccount(models.Model):
    account_number = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    account_type = models.CharField(max_length=20)
    opening_date = models.DateField()
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    aadhar_card_number = models.CharField(max_length=20)
    pan_card_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'personal_bank_account'
   
    def __str__(self):
        return f"{self.account_number}-{self.account_holder_name}"

class RevokeHistory(models.Model):
    ac_no = models.IntegerField()
    date = models.CharField(max_length=255)
    amt = models.IntegerField()
    tr_ty = models.CharField(max_length=255)
    from_ac_no = models.CharField(max_length=255)
    to_ac_no = models.IntegerField()
    voucher_no = models.IntegerField(primary_key=False)
    username = models.CharField(max_length=50)

    class Meta:
        db_table = 'revoke_history'
    def __str__(self):
        return self.voucher_no
        
class FDAccountModel(models.Model):
    fd_ac_no = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    opening_date = models.DateField()
    int_rate = models.DecimalField(max_digits=5, decimal_places=2)
    fd_days = models.IntegerField()
    pre_mature_withdraw = models.BooleanField(default=False)
    mat_amt = models.IntegerField(null=True)
    fd_opening_amt = models.IntegerField()
    personal_ac_no = models.IntegerField()
    fd_mat_dt = models.DateField(null=True)
    renew = models.IntegerField()
    username = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    class Meta:
            db_table = 'fd_accounts'
    def __str__(self):
          return self.customer_name

class RDAccountModel(models.Model):
    rd_ac_no = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    opening_date = models.DateField()
    int_rate = models.DecimalField(max_digits=5, decimal_places=2)
    rd_mat_date = models.DateField(null=True)
    rd_amt = models.DecimalField(max_digits=10, decimal_places=2)
    pre_mature_withdraw = models.BooleanField(default=False)
    username = models.CharField(max_length=255)
    renew = models.IntegerField()
    personal_ac_no = models.IntegerField()
    rd_months = models.IntegerField()
    mat_amt=models.DecimalField(max_digits=10, decimal_places=2)
    int_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        db_table = 'rd_accounts'
    def __str__(self):
        return self.customer_name

class FDLoan(models.Model):
    fd_account = models.OneToOneField(
        FDAccountModel,
        on_delete=models.CASCADE,
        related_name="loan"
    )
    customer_name = models.CharField(max_length=100)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    loan_term = models.IntegerField()
    loan_start_date = models.DateField()
    loan_end_date = models.DateField()
    emi = models.DecimalField(max_digits=15, decimal_places=2)
    outstanding_principal = models.DecimalField(max_digits=15, decimal_places=2)
    interest_due = models.DecimalField(max_digits=15, decimal_places=2)
    total_payment_due = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'FD_Loans'
    def __str__(self):
        return self.Customer_Name
        

class MasterTable(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    password = models.CharField(max_length=255)
    email_id = models.CharField(max_length=255, blank=True, null=True)
    mo_no = models.IntegerField(blank=True, null=True)
    licence_no = models.CharField(max_length=255, blank=True, null=True)
    aadhar = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    dir_name = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        db_table = 'master_table'
    def __str__(self):
        return self.bank_name
        

class Other(models.Model):
    username = models.CharField(max_length=50, primary_key=True)
    voucher_no = models.IntegerField()

    class Meta:
        db_table = 'other'
    def __str__(self):
        return self.username
            