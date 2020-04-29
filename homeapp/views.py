from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from homeapp.forms import LoginForm,RegisterForm,AddressForm,Membershipform
from django.contrib.auth import login,logout,authenticate
from homeapp.models import Membership,Address
from homeapp.urlredirect import UrlRedirect
from products.models import CostProcessing,Product,ProductSize,ProductColor,Tracker
from productsdisplay import views
from homeapp.session import session_cart_create
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from homeapp.activitytracker import CheckIfProductNotIncart,Activity_function,ProductInCart
from django.db.models import Q


# order template view
def Order(request):
    cart,session = session_cart_create(request)
    address = None
    form  = None
    upadate= False
    if not request.user.is_authenticated:
        address =  Address.objects.filter(session=session)
        if not address:
            print('submit address called')
            update=False
            form=AddressForm(request.POST or None)
            if request.method=="POST":
                
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.session=session
                    instance.save()
                    
                    return redirect('billing:billingaddress')
        else:
            update=True
            address = Address.objects.get(session=session)
            form = AddressForm(request.POST or None,instance=address)
            if request.method=="POST":
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.save()
                    return redirect('billing:billingaddress')


    if  request.user.is_authenticated:
        if request.user.is_seller :
            return redirect('homeapp:address')  

        address =  Address.objects.filter(Q(user=request.user) | Q(session=session))
        if not address:
            print('submit address called')
            update=False
            form=AddressForm(request.POST or None)
            if request.method=="POST":
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.session=session
                    instance.user = request.user
                    instance.save()
                    return redirect('billing:billingaddress')
        else:
            update=True
            addinst=address.last()
            if addinst.user is None:
                ddinst.user= request.user
                addinst.save()
            addresinstance= Address.objects.get(user=request.user)
            form = AddressForm(request.POST or None,instance=addresinstance)
            if request.method=="POST":
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.user=request.user
                    instance.save()
                    return redirect('billing:billingaddress')
    template_name="homeapp/order.html"
    context={'update':update,'form':form,'cart':cart}
    return render(request,template_name,context)



def cart(request):
    if  request.user.is_authenticated:
        if request.user.is_seller :
            return redirect('homeapp:address') 
    cartdisply=True
    cart,session = session_cart_create(request)
    pds  = cart.products.all()
    context={'products':pds,'cart':cart}
    template_name="homeapp/cart.html"
    return render(request,template_name,context)



# adding product to cart 
def AddToCart(request,slug):
    product  = get_object_or_404(Product,slug=slug)
    tracker  = Tracker.objects.filter(productdisplay=product).first()
    activity = Activity_function(request)
    sizeobj  = None
    colorobj = None
    cart,session = session_cart_create(request)
    if request.is_ajax():
        colorid  = request.GET.get('colors')
        print(colorid)
        sizeid   = request.GET.get('sizes')
        quantity = request.GET.get('qt')
        colorid =int(colorid)
        sizeid = int(sizeid)
        quantity=int(quantity)
        # check to make sure product quantity is greater than 0
        # before performing  actions.
        if quantity >=0:
            # check to make sure sizeid has a value
            if sizeid > 0:
                #get product size object
                sizeobj = ProductSize.objects.get(id=sizeid)
            # check to make sure colorid has a value 
        if colorid > 0:
            colorobj = ProductColor.objects.get(id=colorid)

            #retrieve, update , create cost processing object for product
        pobj = CostProcessing.objects.filter(product=product)
        if pobj:
            instance = pobj.first()
            #update
            instance.color    = colorobj
            instance.size     = sizeobj
            instance.quantity = quantity
            instance.save()
            pobj =instance
            cart.products.add(pobj)
            cart.save()
        else:
            # create
            pobj= CostProcessing.objects.create(product=product,color=colorobj,size=sizeobj,quantity=quantity)
            cart.products.add(pobj)
            cart.save()
        #update product tracker object
        tracker.productincart=True
        tracker.save()  

    CheckIfProductNotIncart(request)
    data={'cart':cart.pdcount}
    return JsonResponse(data)


# remove product from cart
def RemoveProduct(request):
    cart,session = session_cart_create(request)
    activity = Activity_function(request)
    productId = request.GET.get('remove')
    if int(productId) > 0 :
        getproduct=CostProcessing.objects.get(id=productId)
        cart.products.remove(getproduct)
        cart.save()
        '''
        remove this product from product in cart list activity
        '''
        activity.pdincart.remove(getproduct.product)
        '''
        add this product in remove in cart activity list
        '''
        activity.removeincart.add(getproduct.product)
        return redirect('homeapp:mycart')




#update cart :

'''
Onchange quantity in user cart.
update user cart object
'''
def CartUpdate(request):
    if request.is_ajax():
        cart,session = session_cart_create(request)
        qt           = request.GET.get('cqt')
        pdprocesssx = request.GET.get('pd-process')
        #get product processing object.
        """
        this object stores information related a product
        such as product quantity, selected product color 
        etc.
        """
        processObj  = CostProcessing.objects.get(id=pdprocesssx)
        processObj.quantity= qt
        processObj.save()

        cost= processObj.cost
        sale = processObj.costaftersales
        cart.save()
        objs={
            'sum':cart.total,
            'pdcount':cart.pdcount,
            'sale':sale,
            'cost':cost
        }
        #update cart object
        
        data={'objs':objs}
        return JsonResponse(data)

# show more products to user 
def Shopmore(request):
    pass

# product detail 
def ProductDetail(request,slug):
    
    cartdisply=True
    '''
    call the tracker object for this product
    and update the tracker to viewed
    '''
    product = get_object_or_404(Product,slug=slug)
    # call a function to check if this product 
    # has been added to cart. This function is found
    # in \homeapp\session.py 
    firstsim,simpd=views.SimilarPd(request,productobj=product)
    incart=ProductInCart(request,product)
    mstpp,firstp = views.pp_view(request)
    if product:
        cart,session = session_cart_create(request)
        if not cart:
            cart=None
        else:
            cart = cart.pdcount
        try:
            
            #update tracker object for this product
            track = Tracker.objects.filter(productdisplay=product,viewed=False).first()
            if track:
                #increament product view
                product.views +=1
                product.save()
                
                track.viewed=True
                track.save()
            
        except ObjectDoesNotExist:
            return redirect('homeapp:home')
    # display six  pp_view products to shopper, after they have added a product to cart
    context={'similarfirst':firstsim,'mstpp':mstpp,'simpd':simpd,'cart':cart,'incart':incart,'trending':mstpp,'product':product,'cartdisply':cartdisply}
    template_name="homeapp/productdetail.html"
    return render(request,template_name,context)

    

# home page view
def index(request):
    cartdisply=True
    cart,session = session_cart_create(request)
    mstpp,firstpp = views.pp_view(request)
    #check if this page is requested by seller
    if request.user.is_authenticated:
        if request.user.is_seller :
            return redirect('homeapp:address')
        else:
            return redirect('homeapp:home')
        # If requested by admin
        if request.user.is_admin:
            pass
    # display 10 random products to visitors
    tenpds = views.FirstTen(request)
    context={'firstpp':firstpp,'mstpp':mstpp,'cartdisply':cartdisply,'cart':cart.pdcount,'tenpds':tenpds}
    template_name='homeapp/index.html'
    return render(request,template_name,context)

# view to register sellers 
def register_seller(request):
  
    if request.user.is_authenticated:
        return redirect('homeapp:home')
    
    form          = RegisterForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        user      = form.save(commit=False)
        password  = form.cleaned_data['password']
        email     = form.cleaned_data['email']
        fname     = form.cleaned_data['firstname']
        lname     = form.cleaned_data['lastname']
        number    = form.cleaned_data['number']
        gender    = form.cleaned_data['gender']
        user.set_password(password)
        user.save()
        # set user as seller
        user.seller= True
        # reference the user to self
        user.me =user
        user.save()
        login(request,user)
        return redirect('homeapp:address')
    seller= True
    context = {'form':form,'seller':seller}
    template_name="homeapp/register.html"
    return render(request,template_name,context)




#user address setup

def address_set_up(request):

    # check if view is requested by authenticated user
    if request.user.is_authenticated:
        #check if user has already setup an address
        address_obj = Address.objects.filter(user=request.user).first()
        if address_obj:
            return redirect('homeapp:members')

        form=AddressForm(request.POST or None)
        if form.is_valid():
            if request.method=="POST":
                instance=form.save(commit=False)
                instance.user=request.user
                instance.save()
                return redirect('homeapp:members')
        context={'form':form}
        template_name="homeapp/addresssetup.html"

        return render(request,template_name,context)
    else :
        return redirect('homeapp:home')


#membership view
def membership(request):
    if request.user.is_authenticated:
        #check if user is a seller
        if request.user.is_seller:
            #check if user has setup membership 
            membership_obj = Membership.objects.filter(user=request.user).first()
            if membership_obj:
                return redirect('homeapp:useradmin')
            form = Membershipform(request.POST or None)
            if form.is_valid():
                if request.method=="POST":
                    instance = form.save(commit=False)
                    instance.user= request.user
                    instance.save()
                    return redirect('homeapp:useradmin')
            template_name = "homeapp/membership.html"
            context       = {'form':form}
            return render(request,template_name,context)
        else:
            return HttpResponse('Bad request')
    else:
        return redirect('homeapp:home')

# function for user admin pannel

def UserAdmin(request):
    # call the url redirect function 
    # that will do checks and redirect user base on their state
    if request.user.is_authenticated:
        if request.user.is_seller:
            membership_obj = Membership.objects.filter(user=request.user).first()
            address_obj = Address.objects.filter(user=request.user).first()
           # check if seller has setup membership or address
           #if one not setup, user redirect to homeredirect for url checkup
            if not membership_obj or not address_obj:
                return redirect('homeapp:homeredirect')
    else:
        return redirect('homeapp:homeredirect')

    # redirect the user to admin pannel
    return redirect('pannel:userpannel')


def Logout(request):

    logout(request)
    return redirect('homeapp:home')


#login user 
# login user in to their account
def Login(request):
    if request.user.is_authenticated:
        return redirect('homeapp:home')
    form = LoginForm(request.POST or None)
    if request.method=="POST":
        
        if form.is_valid():
            print('valid')
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            print(username,password)
            user = authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('homeapp:homeredirect')
    context = {'login':form}
    template_name="homeapp/login.html"
    return render(request,template_name,context)