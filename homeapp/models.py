from django.db import models
import sys
import random
import string  
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from .slug import Generate_slug
from django.contrib.contenttypes.models import ContentType


class UserManger(BaseUserManager):
    def  create_user(self,email,password=None,is_active=True,is_admin=False,is_staff=False):
        if not email:
            raise ValueError('User must have an email')
        if not password:
            raise ValueError('User must have password')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user
    def create_staff(self,email,password=None):
        user = self.create_user(email,password=password,is_staff=True)

    def create_superuser(self,email,password=None):
        user = self.create_user(email,password=password,is_staff=True,is_admin=True)
        return user
class CustomUser(AbstractBaseUser):
    gen=(('Male','Male'),('Female','Female'))
    created      = models.DateTimeField(auto_now_add=True,null=True)
    slug         = models.SlugField(null=True)
    dp           = models.ImageField(upload_to='profile',null=True,blank=True)
    email        = models.EmailField(null=True,unique=True)
    firstname    = models.CharField(max_length=225,null=True)
    lastname     = models.CharField(max_length=225,null=True)
    gender       = models.CharField(max_length=100,choices=gen,null=True) 
    active       = models.BooleanField(default=True)
    number       = models.CharField(max_length=12,null=True)
    admin        = models.BooleanField(default=False)
    staff        = models.BooleanField(default=False)
    approve      = models.BooleanField(default=False)
    seller       = models.BooleanField(default=False)
    buyer        = models.BooleanField(default=False)
    me           = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=[]# creating super user
    objects= UserManger()


    class Meta:
        managed= True
    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active 


    @property
    def is_seller(self):
        return self.seller
    @property
    def is_buyer(self):
        return self.buyer
    @property
    def is_app(self):
        return self.approve

    def save(self,*args,**kwargs):

        if not self.id or not self.slug:
            slugv = str(self.firstname) + str(self.lastname)
            instance = self
            #generate slug when ever user model iscreated
            slug = Generate_slug(instance,slugv)
            self.slug=slug
        return super(CustomUser,self).save(*args,**kwargs)

# seller membership model
class Membership(models.Model):
    chone=(('Per Sale','Pay per Sale'),('Subscription','Subscription')) 
    chtwo =(('Yes','Yes'),('No','No'))
    chthree=(('wholesale','Wholesale'),('Retail','Retail'))
    membership    = models.CharField(choices=chone,max_length=30,null=True)
    affilates     = models.CharField(choices=chtwo,max_length=30,null=True)
    sellingmethod = models.CharField(choices=chthree,max_length=30,null=True)
    user          = models.ForeignKey(CustomUser,related_name="membership",on_delete=models.CASCADE,null=True)
    created       = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return "{user}".format(user=self.user)

# save user delivery address

class Address(models.Model):
    created   = models.DateTimeField(auto_now_add=True,null=True)
    user      = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name="address")
    address1  = models.CharField(max_length=150,null=True)
    address2  = models.CharField(max_length=200,null=True,blank=True)
    town      = models.CharField(max_length=100,null=True)
    region    = models.CharField(max_length=200,null=True)

    def __str__(self):
        return "{user}".format(user=self.user)

# save seller ID info
class SellerID(models.Model):
    created   = models.DateTimeField(auto_now_add=True,null=True)
    user      = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name="identification")
    idpic     =  models.ImageField(upload_to="ids",null=True)
    idnum     = models.IntegerField(null=True)

    def __str__(self):
        return '{user}'.format(user=self.user)


# save user try period 
class TryPeriod(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True)
    user    = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="tryp",null=True)
    active  = models.BooleanField(default=True)

# save user premium period 

'''
this model is to save user status 
if user  is premium
'''
class  Premium(models.Model):
    created = models.DateTimeField(auto_now_add=True,null=True)
    user    = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="premiump",null=True)
    active  = models.BooleanField(default=True)
    exp     = models.DateTimeField(null=True)

    def save(self,*args,**kwargs):
        if not self.id:
            # run calculation to calculate exp of premium activation
            pass

        return super(Premium,self).save(*args,**kwargs)



