# file control logic 
from django.utils import six
from datetime import datetime, timezone
from homeapp.models import Premium
from homeapp.models import CustomUser,TryPeriod
import time
import threading
from datetime import timedelta 



# this logic will check user's account info
# Such as
#  when user account was created
# If user is verified 
# If user is premium
# if premium active

def Userstatus():
    # get the current date and time
    todays_date         = datetime.now(timezone.utc)
    #get the current active status object instance
    userstate           = Premium.objects.filter(active=True).first()

    #get all users except admin users and staff users
    users = CustomUser.objects.all().exclude(admin=True).exclude(staff=True)

    #loop through the users 

    for user in users:
        #get the created date of each user
        created =user.created
        #get how old user account is 
        age  = todays_date-created
        date = timedelta(days=30)
        if age==date:
            #call a function to update user tryperiod
            Try_period_update(user)
        else:
            #create active try period objects
            create_try(user) 

"""
modify data base .
This function will update user try period.

This function should be called when ever user's
account is older than 2months
"""

def Try_period_update(user):
    #get user object  instance
    userinstance  = CustomUser.objects.filter(me=user).first()
     #get try period model
    usertryperiod = TryPeriod.objects.filter(user=userinstance).first()
    #update try period model 
    if usertryperiod:
        usertryperiod.active= False
        usertryperiod.save()
        print(usertryperiod.active)

    # if no Try Period object for user
    else:
        # call create try period function and update database
        obj=create_try(user)
        obj.active= False
        obj.save()
        print(obj.active)


# Create and register user try period.

def create_try(user):
    usertryperiod = TryPeriod.objects.filter(user=user).first()
    if not usertryperiod:
        usertryperiod=TryPeriod.objects.create(user=user)
    return usertryperiod
    

     




