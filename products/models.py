from django.db import models
from homeapp.slug import Generate_slug
from .productid import Productid
from homeapp.models import CustomUser
from decimal  import Decimal as D

import sys
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

#category model 

class Category(models.Model):
    name    = models.CharField(max_length=50,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    slug    = models.SlugField(null=True,blank=True)

    def __str__(self):
        return self.name
    def save(self,*args,**kwargs):
        if not self.id:
            slug = self.name
            instance = self
            # callling the generate slug method
            gslug= Generate_slug(instance,slug)
            self.slug = gslug
        return super(Category,self).save(*args,**kwargs)

# sub category model 
   
class SubCategory(models.Model):
    slug    = models.SlugField(null=True,blank=True)
    name     = models.CharField(max_length=100,null=True)
    descrip  = models.TextField()
    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if not self.id:
            slug = self.name
            instance = self
            # calling the slug method that will generate slug
            gslug= Generate_slug(instance,slug)
            self.slug = gslug
        return super(SubCategory,self).save(*args,**kwargs)

# product model 

class Product(models.Model):
    stt=(('posted','posted'),('pending','pending'),('sold','sold'))
    st=(('Brand New','Brand New'),('Used','Used'))
    sl=((0,0),(20,20),(30,30),(35,35),(40,40),(45,45),(50,50),(60,60),(70,70),(80,80))
    created        = models.DateTimeField(auto_now_add=True,null=True)
    category       = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="product_category")
    subcategory    = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="product_subcategory")
    productname    = models.CharField(max_length=50,null=True)
    picone         = models.ImageField(upload_to="productimage",null=True,blank=True)
    pictwo         = models.ImageField(upload_to="productimage",null=True,blank=True)
    picthree       = models.ImageField(upload_to="productimage",null=True,blank=True)
    picfour        = models.ImageField(upload_to="productimage",null=True,blank=True)
    descript       = models.TextField(null=True)
    brand          = models.CharField(max_length=100,null=True)
    model          = models.CharField(max_length=100,null=True)
    size           = models.CharField(max_length=100,null=True)
    color          = models.CharField(max_length=50,null=True)
    slug           = models.SlugField(null=True,blank=True)
    location       = models.CharField(null=True,max_length=200)
    user           = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="userproduct")
    status         = models.CharField(max_length=200,null=True,choices=stt,default="pending")
    state          = models.CharField(max_length=200,null=True,choices=st)
    uniqueid       = models.CharField(max_length=200,null=True,blank=True,unique=True)
    sales          = models.IntegerField(choices=sl,default=0 )
    pdprice        = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    salesprice     = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return self.productname
 
    def save(self,*args,**kwargs):
        self.picone = self.compressImage(self.picone)
        #check if product has a generated uiqueid
        # unique id has a length of 14 characters starting with 
        # composes of 5 characters of user name, 5 characters of product name, and four random characters

        if not self.uniqueid:
            instance    = self
            username    = self.user.firstname
            productname = self.productname 
            pd_id =Productid(instance,username,productname)
            # set the product id
            self.uniqueid = pd_id
        # calculate price of product after sales
        if self.sales >0:
            #price after sale
            sale  = D(self.sales)/100
            price = D(self.pdprice)
            self.salesprice=price-(price * sale)


        if not self.id:
            slug = self.productname
            instance = self
            # calling the slug method that will generate slug
            gslug= Generate_slug(instance,slug)
            self.slug = gslug
        
        return super(Product,self).save(*args,**kwargs)

    def compressImage(self,uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (250,300) ) 
        imageTemproaryResized.save(outputIoStream , format='JPEG', quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


"""
Save quantity purchased,
save price,
save selling price,
save if product on sale.
Perform mathematical calculation to calculate
actual product cost added to cart.
"""
class CostProcessing(models.Model):
    product  = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    cost     = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    salesprice    = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return str(self.product.productname) 

    def save(self,*args,**kwargs):
        qt  = self.quantity
        pr  = self.product.price
        # get the actual 
        cst = D(qt)*D(pr)
        self.cost= cst
        #calculate price of product after salesoff
        sales = self.product.ifsales
        if sales:
            salesoff        = self.product.sales
            percentageoff   = D(salesoff/100) 
            sl              = cst *  percentageoff
            self.salesprice = cst-sl
            

        return super(calculateprice,self).save(*args,**kwargs)

    





