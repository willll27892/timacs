from products.models import Product,Cart
from homeapp.models import Sessionlog
from django.http import HttpRequest



#get user ip 

def userIP(request):
    client_address= request.META.get('HTTP_X_FORWARDED_FOR')
    if client_address:
        ip = client_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# get and create user session


def session_cart_create(request):
    ip=userIP(request)
    #get users ip
    
    # call the create retrieve session function
    session=Create_get_session(request,ip=ip)
    cart = Create_Crud_cart(request,sessionObj=session)
    return cart,session

"""
function which creates and retrieve session 
object
"""
def Create_get_session(request,ip):
    session_id =  request.session.get('session_id',None) 
    session = None
    sessionobj = Sessionlog.objects.filter(id=session_id)
    if not sessionobj:
        session=Sessionlog.objects.create(ip=ip)
        request.session['session_id']= session.id
        print('create called')
        
        return session

    if not request.user.is_authenticated and sessionobj:
        #get sessionlog for this session
        session = Sessionlog.objects.get(id=session_id)

        return session
       
    if request.user.is_authenticated and sessionobj:
        sessioninstance      = Sessionlog.objects.get(id=session_id)
        authsession          = Sessionlog.objects.filter(user=request.user)
        #update the sessionlog with the currently login user
        if not authsession:
            sessioninstance.user = request.user
            sessioninstance.save()
        session = Sessionlog.objects.get(user=request.user)
        return session

# function to get create update cart 
def Create_Crud_cart(request,sessionObj):
    print(sessionObj)
    cart = None
    cartobj = Cart.objects.filter(session=sessionObj,active=True)
    if not request.user.is_authenticated:
        if not cartobj:
            cart = Cart.objects.create(session=sessionObj)
        if cartobj:
            cart = cartobj.first()
        return cart 

    if request.user.is_authenticated:
        print('cart auth')
        cartobtwo = Cart.objects.filter(session=sessionObj,active=True,owner=request.user)
        if cartobj and not cartobtwo:
            print('True')
            cartinstance       = cartobj.first()
            cartinstance.owner = request.user
            cartinstance.save()
            cart = cartinstance
        if  cartobtwo:
            cart = cartobtwo.first()
        if not cartobj and not cartobtwo:
            cart = Cart.objects.create(session=sessionObj,owner=request.user)

        return cart

    



    

