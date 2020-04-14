from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from products.models import Product,Tracker
from homeapp.session import session_cart_create



"""
track all the products user has visited
using the session id
"""
class Activity(models.Model):
    session         = models.CharField(max_length=200,null=True)
    display         = models.ManyToManyField(Tracker,related_name="display")
    products        = models.ManyToManyField(Product,related_name="products")
    pdnotincart     = models.ManyToManyField(Product,related_name='pdcart')

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
    session    = session_cart_create(request)
    sessionid  = session.id
    productobj = products 
    activity   = trackproducts(productobj,sessionid)
    return activity
 


'''
this function call is very important.
Here the magic is, this will make things
possible to easily track  user activity base on their
registered session id. Knowing what product 
the user has viewed and making sure viewed products
do not repeat themselves to themsame user.
'''
def  trackproducts(productobj,sessionid):
    '''
    Activity object is called. This object stores product objects
    and tracker objects
    '''
    activity = Activity.objects.filter(session=sessionid)
    #check if activity object for this session id has been created
    if activity:
        # assumming this is the 1 + call to this function
        # get the first Activity object
        activity = Activity.objects.filter(session=sessionid).first()
        #get all the products in Activity object
        productlogs = activity.products.all()
        for product in productobj:
            #check if product has been tracked before creating a tracker object for it
            if not product in productlogs:
                Tracker.objects.create(productdisplay=product,session=sessionid) 

    if not activity:
        activity = Activity.objects.create(session=sessionid)
        # create product tracker objects  for this session id
        for product in productobj:
            Tracker.objects.create(productdisplay=product,session=sessionid)

            
            
    for product in productobj:
        activity.products.add(product)
    activity =Activity.objects.filter(session=sessionid).first()
    return activity

def CheckIfProductNotIncart(request,objs):
    session    = session_cart_create(request)
    sessionid = session.id
    #get all products in cart intance of current user
    activity = Activity.objects.filter(session=sessionid).first()
    products = session.products.all()

    print(products.count())
    print(objs.count())
    for  obj in objs:
        # loop through cart product objects
        for product in products:
            # check if track product is in card 
            if not product.product == obj.productdisplay:
                # add all  track products not in cart in a activity
                # list
                activity.pdnotincart.add(obj.productdisplay)
            # if product is in cart, update product tracker object
            if product.product == obj.productdisplay:
                obj.productincart =True
                obj.save()
    # return activity object
    activity = Activity.objects.filter(session=sessionid).first()

    return activity 
    #check if 