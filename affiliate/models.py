from django.db import models
from homeapp.models import CustomUser

# Create your models here.

class Application(models.Model):
    created    = models.DateTimeField(null=True,)
    user       = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="affiliate",null=True)
    email      = models.EmailField(null=True)
    number     = models.IntegerField(null=True)
    name       = models.CharField(null=True,max_length=200)
    address    = models.TextField(null=True)
    occupation = models.CharField(null=True,max_length=200)
