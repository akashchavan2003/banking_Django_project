# Generated by Django 4.1.13 on 2024-04-14 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_alter_cashtransaction_cash_in_hand_previous'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashtransaction',
            name='narration',
            field=models.TextField(default=''),
        ),
    ]
