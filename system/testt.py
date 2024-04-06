from models import CashInHand


# Retrieve the record you want to update
record = CashInHand.objects.get(username="DEO10167")

# Update the field
record.cash_in_hand = 67
print("done")
# Save the changes
record.save()