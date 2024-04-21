from models import PersonalBankAccount
user="DEO10167"
columns = PersonalBankAccount.objects.filter(username=user).values()
for column in columns:
        print(column)