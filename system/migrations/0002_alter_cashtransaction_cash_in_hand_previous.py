# Generated by Django 4.1.13 on 2024-04-03 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashtransaction',
            name='cash_in_hand_previous',
            field=models.CharField(default='N', max_length=255),
        ),
    ]
