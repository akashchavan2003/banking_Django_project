import datetime

from system.models import MasterTable
from system.bank_managament_system import get_current_date
# this is for the updating all templates from the database 
# like all the extending the base.html are all updates through this context_processors.py
# we can add more like this content in this
def custom_context(request):
    user = request.user.username
    reg_No=0
    try:
        # Query the MasterTable model to get the record for the current user from the other database
        master_record = MasterTable.objects.using('other_database').get(username=user)
        bank_name = str(master_record.bank_name).upper()
        dir_name = str(master_record.dir_name).upper()
        reg_No=str(master_record.licence_no)
        dt=get_current_date()
        url= '/media/bank_logo.jpg'
    except MasterTable.DoesNotExist:
        bank_name = None
        dir_name = None
        dt="0"
        url= '/media/bank_logo.jpg'
    return{'bank_name': bank_name,
        'name': dir_name,'reg_no':reg_No,'date':dt,'firm_name':bank_name,'photo_url':url}