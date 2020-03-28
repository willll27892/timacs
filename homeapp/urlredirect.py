# this  file is handle url processing and redirecting users
# to the right urls and views.

from homeapp.models import  CustomUser,Address,Membership
from django.shortcuts import render,redirect


# function to handle urls redirect
# users will be directed to their respective pages base on their status

def UrlRedirect(request):
    
    if not request.user.is_authenticated:
        #if user not authenticated, redirect the user to home page
        return redirect('homeapp:home')
    if request.user.is_authenticated:
        getaddress     = Address.objects.filter(user=request.user).first()
        getmembership  = Membership.objects.filter(user=request.user).first()
        
        #check if user is admin 
        if request.user.is_admin:
            # redirect the user to admin page
            pass
        #check if user is buyer 
        if request.user.is_buyer:
            #redirect user to buyer page
            pass

        # check if user is seller

        if request.user.is_seller:
            #check if authenticated user has setup address
            if not getaddress:
                #redirect user to setup address
                return redirect('homeapp:address')
            if getaddress:
                # redirect user to setup membership
                return redirect('homeapp:members')

            #check if authenticated user has setup membership
            if not getmembership:
                return redirect('homeapp:members')
            if getmembership:
                return redirect('homeapp:useradmin')

