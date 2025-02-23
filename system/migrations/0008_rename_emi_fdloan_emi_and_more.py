# Generated by Django 4.1.13 on 2024-12-25 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_rdaccountmodel_int_earned'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fdloan',
            old_name='EMI',
            new_name='emi',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='FD_Amount',
            new_name='fd_amount',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Interest_Due',
            new_name='interest_due',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Interest_Rate',
            new_name='interest_rate',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Loan_Account_Number',
            new_name='loan_account_number',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Loan_Amount',
            new_name='loan_amount',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Loan_End_Date',
            new_name='loan_end_date',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Loan_Start_Date',
            new_name='loan_start_date',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Loan_Term',
            new_name='loan_term',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Outstanding_Principal',
            new_name='outstanding_principal',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Status',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='fdloan',
            old_name='Total_Payment_Due',
            new_name='total_payment_due',
        ),
        migrations.AddField(
            model_name='fdloan',
            name='fd_account',
            field=models.OneToOneField(default='null', on_delete=django.db.models.deletion.CASCADE, related_name='loan', to='system.fdaccountmodel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cashinhand',
            name='username',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, unique=True),
        ),
    ]
