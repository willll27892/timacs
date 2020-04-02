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

# product size 

class ProductSize(models.Model):
    user         = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="pdsize",null=True)
    created      = models.DateTimeField(auto_now_add=True,null=True)
    updated      = models.DateTimeField(auto_now=True,null=True)
    size         = models.CharField(max_length=200,null=True)
    sizeprice    = models.IntegerField(null=True)
    pricechange  = models.BooleanField(default=False)

    def __str__(self):
        return str(self.size)

# this model will save product copy in a different color
class ProductColor(models.Model):
    color           = models.CharField(max_length=50,null=True)
    picone          = models.ImageField(upload_to="productimage",null=True)
    pictwo          = models.ImageField(upload_to="productimage",null=True)
    picthree        = models.ImageField(upload_to="productimage",null=True)
    picfour         = models.ImageField(upload_to="productimage",null=True)
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="userproductcolor",null=True)


# product model 

class Product(models.Model):
    stt             = (('posted','posted'),('pending','pending'),('sold','sold'))
    st              = (('Brand New','Brand New'),('Used','Used'))
    sl              = ((0,0),(20,20),(30,30),(35,35),(40,40),(45,45),(50,50),(60,60),(70,70),(80,80))
    created         = models.DateTimeField(auto_now_add=True,null=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="product_category",null=True)
    subcategory     = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name="product_subcategory")
    productname     = models.CharField(max_length=50,null=True)
    picone          = models.ImageField(upload_to="productimage",null=True)
    pictwo          = models.ImageField(upload_to="productimage",null=True)
    picthree        = models.ImageField(upload_to="productimage",null=True)
    picfour         = models.ImageField(upload_to="productimage",null=True)
    descript        = models.TextField(null=True)
    brand           = models.CharField(max_length=100,null=True)
    model           = models.CharField(max_length=100,null=True)
    size            = models.CharField(max_length=100,null=True)
    color           = models.CharField(max_length=50,null=True)
    slug            = models.SlugField(null=True,blank=True)
    location        = models.CharField(null=True,max_length=200)
    user            = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="userproduct",null=True)
    status          = models.CharField(max_length=200,null=True,choices=stt,default="pending")
    state           = models.CharField(max_length=200,null=True,choices=st)
    uniqueid        = models.CharField(max_length=200,null=True,blank=True,unique=True)
    sales           = models.IntegerField(choices=sl,default=0 )
    pdprice         = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=False)
    salesprice      = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    pdcolor         = models.ManyToManyField(ProductColor,related_name="color_id",null=True,blank=True)
    availableseizes = models.ManyToManyField(ProductSize,null=True,related_name="avlprice")
    def __str__(self):
        return self.productname
 
    def save(self,*args,**kwargs):
        """
        Update status of all
        products related to  this product
        """
        if self.status and self.id:
            klass = self.__class__
            obj   = klass.objects.get(id=self.id)
            '''
            get all product colors related to 
            this product post
            '''
            colors = obj.availableseizes.all()

            # check if product post has any product color related to it
            # loop through available colors 
            if colors:
                status = self.status
                colorsave(colors,status)


        self.picone = self.compressImage(self.picone)
        self.pictwo = self.compressImage(self.pictwo)
        self.picthree = self.compressImage(self.picthree)
        self.picfour = self.compressImage(self.picfour)
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
        width,height=imageTemproary.size
        
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize( (250,300) )
        if width>250 and height>300:
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=80)
        if width<250 and height<300:
            imageTemproaryResized.save(outputIoStream , format='JPEG', quality=100)
        if width==250 and height==300:
            imageTemproary.save(outputIoStream , format='JPEG', quality=100)   
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

def colorsave(colors,status):
    for color in colors:
        '''
        update all color object status
        to  the present status of the 
        parent obj
        '''
        color.post=status
        color.save()
"""
save product related product object,
Save quantity purchased of related product object,
get the product price of related product object,
get the product sales price of related product object
If related product object on salesoff, it caculates the actual price after salesoff with respect to 
product quantity ordered
This model is added to user cart, when ever a user add a product to cart
"""
class CostProcessing(models.Model):
    user              = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product           = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity          = models.IntegerField(default=1)
    cost              = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    #product cost after sales
    costaftersales    = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return str(self.product.productname) 

    def save(self,*args,**kwargs):
        qt  = self.quantity
        pr  = self.product.pdprice
        # get the actual 
        cst = D(qt)*D(pr)
        self.cost= cst
        #calculate price of product after salesoff
        if self.product.sales>0:
            salesprice        = self.product.salesprice
            self.costaftersales = salesprice * qt
            

        return super(CostProcessing,self).save(*args,**kwargs)


# product cart model    
class Cart(models.Model):
    owner    = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    created  = models.DateTimeField(auto_now_add=True,null=True)
    updated  = models.DateTimeField(auto_now=True,null=True)
    products = models.ManyToManyField(CostProcessing,related_name="cpds")
    active   = models.BooleanField(default=True)
    pdcount  = models.IntegerField(null=True,blank=True)
    total    = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return str("{owner}".format(owner=self.owner))
    
    def save(self,*args,**kwargs):
        '''
        Calculate the total number of products in cart.
        give the sum amount of all the products in cart.
        Making sure put  consideration on products on sale
        and products not on sale.
        '''
        # if card has been created
        if self.id:
            salesprice    = D(0.00)
            originalprice = D(0.00)
            productcount  = 0
            #now get products from manytomany relationship field
            cartobj       = self.__class__.objects.filter(id=self.id).first()
            pdobjs        = cartobj.products.all()
            # loop through each object and perform mathematical calculations
            for product in pdobjs:
                """
                check all CostProcessing related to products on sales in current cart
                and sum their sales price amount
                """
                if product.product.sales>0:
                    salesprice +=product.costaftersales
                """
                check all CostProcessing related to products not on sales in current cart
                and sum their sales price amount
                """
                if product.product.sales==0:
                    originalprice +=product.cost
                productcount +=product.quantity
            """
            get the total amount user is suppose to pay for the 
            products
            """
            self.total= D(salesprice) + D(originalprice)
            self.pdcount = productcount
        return super(Cart,self).save(*args,**kwargs)







