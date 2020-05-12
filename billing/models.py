from django.db import models
from homeapp.models import Sessionlog
from homeapp.models import CustomUser,Address

class Billing(models.Model):
    btype=(
        (('mastercard','Mastercard'),('VisaCard','VisaCard'),('MobileMoney','Mobile money'))
    )
    contact   = models.CharField(max_length=18,null=True)
    created   = models.DateTimeField(auto_now_add=True,null=True)
    owner     = models.ForeignKey(Sessionlog,on_delete=models.CASCADE,null=True)  
    name      = models.CharField(max_length=200,null=True)
    address   = models.CharField(max_length=200,null=True)
    town      = models.CharField(max_length=200,null=True)
    region    = models.CharField(max_length=200,null=True)
    country   = models.CharField(max_length=200,null=True)
    billtype  = models.CharField(choices=btype,max_length=200,null=True)
    zipcode   = models.CharField(max_length=200,null=True,blank=True)
