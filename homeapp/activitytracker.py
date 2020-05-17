from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from products.models import Product,Tracker,Popular
from homeapp.session import session_cart_create
from homeapp.models import CustomUser


"""
track all the products user has visited
using the session id
"""
class Activity(models.Model):
    state          = models.CharField(max_length=200,null=True)
    popular        = models.ManyToManyField(Product,related_name="popularproduct")
    user           = models.ForeignKey(CustomUser,null=True,related_name='actuser',on_delete=models.CASCADE)
    session        = models.CharField(max_length=200,null=True)
    incart         = models.ManyToManyField(Tracker,related_name="display")
    products       = models.ManyToManyField(Product,related_name="products")
    pdincart       = models.ManyToManyField(Product,related_name='pdcart')
    removeincart   = models.ManyToManyField(Product,related_name="removecart")
'''
activtiy function
this function  creates a tracker object for approved products.
This is very important to monitor which products users have 
viewed in a particular session id. To aviod same viewed
products repeating themselves   to the user.
'''
def Activity_function(request):
    # this should filter approved products
    products   = Product.objects.all()
    #call session activity function 
    # get session id by calling session id function
    cart,session = session_cart_create(request)
    sessionid  = session.id
    pdobjs = products 
    user = request.user
    #call activity tracker object
    activity   = trackproducts(user,pdobjs,sessionid)
    return activity
 


'''
this function call is very important.
Here the magic is, this will make things
possible to easily track  user activity base on their
registered session id. Knowing what product 
the user has viewed and making sure viewed products
do not repeat themselves to same user.
'''
def  trackproducts(user,pdobjs,sessionid):
    '''
    pdobjs = Products.object.all()
    '''
    '''
    Activity object is called. This object stores product objects
    and tracker objects
    '''
    activity = Activity.objects.filter(session=sessionid)
    #check if activity object for this session id has been created
    '''
    add  popular products in to activity popular list
    and create a season tracker objects for popular 
    products
    '''
    #filter all products width views creater than
    # the given number of views from Popular
    minviews= Popular.objects.all().last()
    if not minviews:
        minviews = Popular.objects.create()
    if not user.is_authenticated:
        if activity:
            # assumming this is the 1 + call to this function
            # get the first Activity object
            activity = Activity.objects.filter(session=sessionid).first()
            #get all the products in Activity object
            productlogs = activity.products.all()
            for product in pdobjs:
                #check if tracker object has been created for product
                if not product in productlogs:
                    Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,state=product.state,productdisplay=product,session=sessionid) 
                    # create tracker object for popular product
                    if  product.views > minviews.views:
                        Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,state=product.state,popular=True,productdisplay=product,session=sessionid) 

 
        if not activity:
            activity = Activity.objects.create(session=sessionid)
            # create product tracker objects  for this session id
            for product in pdobjs:
                Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,state=product.state,productdisplay=product,session=sessionid)
                # create tracker object for popular product
                if  product.views > minviews.views:
                    Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,state=product.state,popular=True,productdisplay=product,session=sessionid) 
        
        for product in pdobjs:
            activity.products.add(product)
        activity =Activity.objects.filter(session=sessionid).first()
        '''
        create a
        '''
        return activity


    if user.is_authenticated:
        authactivity = Activity.objects.filter(session=sessionid,user=user)
        if authactivity:
            # assumming this is the 1 + call to this function
            # get the first Activity object
            activity = authactivity.first()
            #get all the products in Activity object
            productlogs = activity.products.all()
            for product in pdobjs:
                #check if tracker object has been created for product
                if not product in productlogs:
                    Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,productdisplay=product,session=sessionid)
                    # create tracker object for popular product
                    if  product.views > minviews.views:
                        Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,popular=True,productdisplay=product,session=sessionid) 
        
        if activity and not authactivity:
            sesactivity =activity.first()
            sesactivity.user=user
            sesactivity.save()
            activity = sesactivity

        if not activity and not  authactivity:
            activity = Activity.objects.create(session=sessionid,user=user)
            # create product tracker objects  for this session id
            for product in pdobjs:
                Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,productdisplay=product,session=sessionid)
                # create tracker object for popular product
                if  product.views > minviews.views:
                    Tracker.objects.create(productname=product.productname,productprice=product.pdprice,productstate=product.state,categoryname=product.category.name,subcategoryslug=product.subcategory.slug,popular=True,productdisplay=product,session=sessionid) 
        for product in pdobjs:
            activity.products.add(product)
        activity =Activity.objects.filter(session=sessionid,user=user).first()

        
        return activity
        
def CheckIfProductNotIncart(request):
    cart,session    = session_cart_create(request)
    #get current active activity object
    activity = Activity_function(request)
    products = cart.products.all()
    # track all products user has added to active cart
    for product in products:
        activity.pdincart.add(product.product) 
    activity = Activity_function(request)        
    # return activity object   
    return activity 
    #check if 

'''
check if current product 
has been added to current active 
cart
'''
def ProductInCart(request,product):
    cart,session = session_cart_create(request)
    activity=Activity_function(request)
    products = activity.pdincart.all()
    print(products.count())

    if product in products:
        return True
    else:
        return False