# this view is to handle product display logics

from products.models import Product,Tracker
from django.db.models import Q
from homeapp.session import session_cart_create
from homeapp.activitytracker import CheckIfProductNotIncart,Activity_function
from products.models import Product

"""
Query and return products to be displayed 
in home page 
"""

# display  first ten  radom products to a visitor
def  FirstTen(request):

    '''
    Activity_function(request)
    this function call is very important.
    Here the magic is, this will make things
    possible to easily track  user activity base on their
    registered session id. Knowing what product 
    the user has viewed and making sure viewed products
    do not repeat themselves to themsame user. and many more
    '''
    # calling the activity function
    Activity_function(request)
    
    cart,session = session_cart_create(request)
    #get the first 10 random approved products.
    '''
    Tracker object is related to product objects.
    Tracker objects are created when activity_function(request)
    called.
    '''
    products = Tracker.objects.filter(Q(viewed=False) & Q(session=session.id) & Q(productincart=False))[:12]
    
    '''
        at this point, the user has viewed all products in the database.
        Now we have to repeat viewed products display back to user,
        but not products already added in user's cart.
        calling CheckIfProductNotIncart() function will 
        perform a logic to check and add all products not in 
        user cart in an activity obj. We can retrieve these
        products when ever needed to avoid showing products
        a user has added to their cart
    '''
    if  products.count() <= 4:
        
        products = Tracker.objects.filter(Q(viewed=True) & Q(session=session.id) & Q(productincart=False))[:12]

        
    return products


# popular products
def Popular(request):
    cart,session= session_cart_create(request)

    #get the first 10 random approved products.
    '''
    Tracker object is related to product objects.
    Tracker objects are created when activity_function(request)
    called.
    '''
    products = Tracker.objects.filter(Q(productdisplay__views__gte=2,productincart=False))[:6]
        
    return products

# display products of similar category
def SimilarPd(request,productobj):
    pdName   = productobj.productname
    pdCat    = productobj.category
    pdSubCat = productobj.subcategory
    pdBrand  = productobj.brand
    products = Product.objects.filter(Q(brand=pdBrand) | Q(productname=pdName) | Q(category=pdCat) | Q(subcategory=pdSubCat)).exclude(id=productobj.id)[:12]
    return products

    
# Suggest Products to user base on user activities
def Suggestion(request):
    pass 

# display promo items

def Promo(request):
    pass