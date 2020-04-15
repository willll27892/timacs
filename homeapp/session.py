from products.models import Product,Cart
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
    print(ip)
    #get users ip
    session_id =  request.session.get('session_id',None)
    cart  =   Cart.objects.filter(id=session_id)
    '''
    create a new cart id for this session
    or retrieve the cart obj for this session if one already exist
    '''
    if not request.user.is_authenticated:
        if cart:
            cart = Cart.objects.first()
        if not cart:
            cart = Cart.objects.create()
            request.session['session_id']= cart.id
        return cart
    # when user has login, check if there is an active cart object
    if request.user.is_authenticated and cart:
        usercart        = Cart.objects.filter(owner=request.user)
        cartinstanceone = cart.first()
        # check if user does not have an existing cart
        # and set the current cart to the present login user
        if not usercart:
            cartinstanceone.owner = request.user
            cartinstanceone.save()
            cart = cartinstanceone
        if  usercart:
            cart.delete()
            cart = usercart.first()
        return cart

    if request.user.is_authenticated and not cart:
        usercart        = Cart.objects.filter(owner=request.user)
        if not usercart:
            cart = Cart.objects.create(owner=request.user)
        if usercart:
            cart=usercart.first()
        return cart


#check if product has been added to card 

def ProductInCart(request,product):
    cart = session_cart_create(request)
    pobjs = cart.products.all()
    product_added_to_cart=False
    # if product is in cart, function will return true
    for processors in pobjs:
        if product.id == processors.product.id:
            product_added_to_cart= True
            print('is in cart')
            return product_added_to_cart
        else:
            print('is not in cart')
            product_added_to_cart= False
            return product_added_to_cart
    

