# Generated by Django 4.1.13 on 2024-03-16 16:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashInHand',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('cash_in_hand', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'db_table': 'cash_in_hand',
            },
        ),
        migrations.CreateModel(
            name='CashTransaction',
            fields=[
                ('ac_no', models.IntegerField()),
                ('transaction_type', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=255)),
                ('amt', models.IntegerField()),
                ('cash_in_hand_previous', models.CharField(max_length=255)),
                ('voucher_no', models.IntegerField()),
                ('frm_ac_no', models.IntegerField()),
                ('to_ac_no', models.IntegerField()),
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'cash_transaction',
            },
        ),
        migrations.CreateModel(
            name='DeletedAccount',
            fields=[
                ('account_number', models.AutoField(primary_key=True, serialize=False)),
                ('account_holder_name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('account_type', models.CharField(max_length=20)),
                ('opening_date', models.DateField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=255)),
                ('aadhar_card_number', models.CharField(max_length=20)),
                ('pan_card_number', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'deleted_ac',
            },
        ),
        migrations.CreateModel(
            name='FDLoan',
            fields=[
                ('Customer_Name', models.CharField(max_length=100)),
                ('Loan_Account_Number', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('FD_Amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Loan_Amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Interest_Rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('Loan_Term', models.IntegerField()),
                ('Loan_Start_Date', models.DateField()),
                ('Loan_End_Date', models.DateField()),
                ('EMI', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Outstanding_Principal', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Interest_Due', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Total_Payment_Due', models.DecimalField(decimal_places=2, max_digits=15)),
                ('Status', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'FD_Loans',
            },
        ),
        migrations.CreateModel(
            name='MasterTable',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=255)),
                ('email_id', models.CharField(blank=True, max_length=255, null=True)),
                ('mo_no', models.IntegerField(blank=True, null=True)),
                ('licence_no', models.CharField(blank=True, max_length=255, null=True)),
                ('aadhar', models.IntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dir_name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'master_table',
            },
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('voucher_no', models.IntegerField()),
            ],
            options={
                'db_table': 'other',
            },
        ),
        migrations.CreateModel(
            name='PersonalBankAccount',
            fields=[
                ('account_number', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('account_holder_name', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('account_type', models.CharField(max_length=20)),
                ('opening_date', models.DateField()),
                ('address', models.CharField(max_length=255)),
                ('mobile_number', models.CharField(max_length=15)),
                ('aadhar_card_number', models.CharField(max_length=20)),
                ('pan_card_number', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'personal_bank_account',
            },
        ),
        migrations.CreateModel(
            name='RevokeHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ac_no', models.IntegerField()),
                ('date', models.CharField(max_length=255)),
                ('amt', models.IntegerField()),
                ('tr_ty', models.CharField(max_length=255)),
                ('from_ac_no', models.CharField(max_length=255)),
                ('to_ac_no', models.IntegerField()),
                ('voucher_no', models.IntegerField()),
                ('username', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'revoke_history',
            },
        ),
    ]
