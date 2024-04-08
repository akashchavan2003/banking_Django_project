from system.models import MasterTable
# this is for the updating all templates from the database 
# like all the extending the base.html are all updates through this context_processors.py
# we can add more like this content in this
def custom_context(request):
    user = request.user.username
    try:
        # Query the MasterTable model to get the record for the current user from the other database
        master_record = MasterTable.objects.using('other_database').get(username=user)
        bank_name = str(master_record.bank_name).upper()
        dir_name = str(master_record.dir_name).upper()
    except MasterTable.DoesNotExist:
        bank_name = None
        dir_name = None
    return{'bank_name': bank_name,
        'name': dir_name,}