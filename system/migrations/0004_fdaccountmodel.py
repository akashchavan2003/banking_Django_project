# Generated by Django 4.1.13 on 2024-04-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_cashtransaction_narration'),
    ]

    operations = [
        migrations.CreateModel(
            name='FDAccountModel',
            fields=[
                ('fd_ac_no', models.IntegerField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=255)),
                ('account_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('opening_date', models.DateField()),
                ('int_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fd_days', models.IntegerField()),
                ('pre_mature_withdraw', models.BooleanField(default=False)),
                ('mat_amt', models.IntegerField(null=True)),
                ('fd_opening_amt', models.IntegerField()),
                ('personal_ac_no', models.IntegerField()),
                ('fd_mat_dt', models.DateField(null=True)),
                ('renew', models.IntegerField()),
                ('username', models.CharField(max_length=255)),
            ],
        ),
    ]