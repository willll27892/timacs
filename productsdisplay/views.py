# this view is to handle product display logics

from products.models import Product,Tracker
from django.db.models import Q
from homeapp.session import session_cart_create
from homeapp.activitytracker import CheckIfProductNotIncart,Activity_function
from products.models import Product,Popular

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
    activity=Activity_function(request)
    
    cart,session = session_cart_create(request)
    #get the first 10 random approved products.
    '''
    Tracker object is related to product objects.
    Tracker objects are created when activity_function(request)
    called.
    '''
    products = Tracker.objects.filter(Q(state="Brand New") & Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[:12]
    
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
        
        products = Tracker.objects.filter(Q(state="Brand New") & Q(popular=False) & Q(viewed=True) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[:12]
    
    if  products.count() <= 4:
        products=None

    return products


# popular products
def pp_view(request):
    cart,session= session_cart_create(request)

    #get the first 10 random approved products.
    '''
    Tracker object is related to product objects.
    Tracker objects are created when activity_function(request)
    called.
    '''
    pp = Popular.objects.all().last()
    if not pp:
        pp    = Popular.objects.create()
    # retrieve all products with views greater and equal to the given view
    postedproducts = Product.objects.filter(views__gte=pp.views) 
    products  = Tracker.objects.filter(Q(state="Brand New") & Q(popular=True,productdisplay__views__gte=pp.views,session=session.id,productincart=False))[:6]
    first     = Tracker.objects.filter(Q(popular=True,productdisplay__views__gte=pp.views,session=session.id,productincart=False)).last()  

    '''
    refresh popular product objects
    '''
    if products.count() <= 6:
        #delete old popular product objects for present session
        for product in products:
            product.delete()
        #create new popular product objects
        for product in postedproducts:
                Tracker.objects.create(state=product.state,productdisplay=product,session=session.id,popular=True)
    # retrieve  new available popular product objects.
    products = Tracker.objects.filter(Q(state="Brand New") & Q(popular=True,productdisplay__views__gte=pp.views,session=session.id,productincart=False))[:6]
    first    = Tracker.objects.filter(Q(popular=True,productdisplay__views__gte=pp.views,session=session.id,productincart=False)).last()    
    return products,first

# display products of similar category
def SimilarPd(request,productobj):
    pdName   = productobj.productname
    pdCat    = productobj.category
    pdSubCat = productobj.subcategory
    pdBrand  = productobj.brand
    products = Product.objects.filter(Q(state="Brand New") | Q(brand=pdBrand) | Q(productname=pdName) | Q(category=pdCat) | Q(subcategory=pdSubCat)).exclude(id=productobj.id)[:12]
    first    = Product.objects.filter(Q(state="Brand New") | Q(brand=pdBrand) | Q(productname=pdName) | Q(category=pdCat) | Q(subcategory=pdSubCat)).exclude(id=productobj.id).first()
    return first,products

    
# Suggest Products to user base on user activities
def Suggestion(request):
    pass 

# display promo items

def Promo(request):
    pass

def UsedProducts(request):
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
    activity=Activity_function(request)
    
    cart,session = session_cart_create(request)
    #get the first 10 random approved products.
    '''
    Tracker object is related to product objects.
    Tracker objects are created when activity_function(request)
    called.
    '''
    products = Tracker.objects.filter(Q(state="Used") & Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[:24]
    
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
        
        products = Tracker.objects.filter(Q(state="Used") & Q(popular=False) & Q(viewed=True) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[:24]
    if  products.count() <= 4:
        products=None
    return products


# display products to the user
def ShopeMore(request):
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
    activity=Activity_function(request)

    
    cart,session = session_cart_create(request)
    print('print session')
    print(session)
    products1 = Tracker.objects.filter( Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[0:10]
    products2 = Tracker.objects.filter( Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[10:20]
    products3 = Tracker.objects.filter( Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')[20:30]
    print(products1)
    return products1,products2,products3


# quick seach from menu category and sub category 

def MenuSearch(request,cat,sub):
    cart,session = session_cart_create(request)
    products = Tracker.objects.filter(Q(subcategoryslug=sub) & Q(categoryname=cat) & Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')
    return products


def SearchCategory(request,catname):
    cart,session = session_cart_create(request)
    products = Tracker.objects.filter( Q(categoryname=cat) & Q(popular=False) & Q(viewed=False) & Q(session=session.id) & Q(productincart=False)).order_by('-created')
    return products