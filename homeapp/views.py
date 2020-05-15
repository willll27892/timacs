from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from homeapp.forms import LoginForm,RegisterForm,AddressForm,Membershipform
from django.contrib.auth import login,logout,authenticate
from homeapp.models import Membership,Address,Sagreement
from homeapp.urlredirect import UrlRedirect
from products.models import CostProcessing,Product,ProductSize,ProductColor,Tracker
from productsdisplay import views
from homeapp.session import session_cart_create
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from homeapp.activitytracker import CheckIfProductNotIncart,Activity_function,ProductInCart
from django.db.models import Q
from order.forms import ReceiverInfo
from order.models import ReceiversName,ProductOrder,Orderstatus
from productsdisplay.views import UsedProducts,ShopeMore


def selleragreement(request):
    agmnt = Sagreement.objects.all().last()
    context={'agmnt':agmnt}
    template_name="homeapp/agreement.html"
    return render (request,template_name,context)

# setup or return delivery address and receiver 
def Order(request):
    cart,session = session_cart_create(request)
    address = None
    form  = None
    receiverform = None
    update= False
    receiverobj =False
    if not request.user.is_authenticated:
        receiver = ReceiversName.objects.filter(session=session)
        address  =  Address.objects.filter(session=session)
       #check if receiver object has been created 
        if not receiver:
            receiverobj =False
            receiverform  = ReceiverInfo(request.POST or None)

        if receiver:
            receiverobj=True
            receiver=ReceiversName.objects.get(session=session)
            receiverform  = ReceiverInfo(request.POST or None,instance=receiver)
         
        
        if not address:
            print('submit address called')
            update=False
            form=AddressForm(request.POST or None)
            if request.method=="POST":
                
                if form.is_valid() and receiverform.is_valid():
                    instance1 = receiverform.save(commit=False)
                    instance1.session=session
                    instance1.save()
                    instance = form.save(commit=False)
                    instance.session=session
                    instance.save()
                    
                    return redirect('billing:billingaddress')
        else:
            update=True
            address = Address.objects.get(session=session)
            form = AddressForm(request.POST or None,instance=address)
            if request.method=="POST":
                if form.is_valid() and receiverform.is_valid():
                    instance1 = receiverform.save(commit=False)
                    instance1.session=session
                    instance1.save()                    
                    instance=form.save(commit=False)
                    instance.save()
                    return redirect('billing:billingaddress')


    if  request.user.is_authenticated:
        if request.user.is_seller :
            return redirect('homeapp:address')  
        receiver = ReceiversName.objects.filter(session=session)
        address =  Address.objects.filter(Q(user=request.user) | Q(session=session))
       #check if receiver object has been created 
        if not receiver:
            receiverobj =False
            receiverform  = ReceiverInfo(request.POST or None)
        if receiver:
            receiverobj=True
            receiver=ReceiversName.objects.get(session=session)
            receiverform  = ReceiverInfo(request.POST or None,instance=receiver)
         
        if not address:
            print('submit address called')
            update=False
            form=AddressForm(request.POST or None)
            if request.method=="POST":
                if form.is_valid() and receiverform.is_valid():
                    instance1 = receiverform.save(commit=False)
                    instance1.session=session
                    instance1.save() 
                    instance = form.save(commit=False)
                    instance.session=session
                    instance.user = request.user
                    instance.save()
                    return redirect('billing:billingaddress')
        else:
            update=True
            addinst=address.last()
            if addinst.user is None:
                addinst.user= request.user
                addinst.save()
            addresinstance= Address.objects.get(user=request.user)
            form = AddressForm(request.POST or None,instance=addresinstance)
            if request.method=="POST":
                if form.is_valid() and receiverform.is_valid():
                    instance1 = receiverform.save(commit=False)
                    instance1.session=session
                    instance1.save() 
                    instance=form.save(commit=False)
                    instance.user=request.user
                    instance.save()
                    return redirect('billing:billingaddress')
    template_name="homeapp/order.html"
    context={'receiverobj':receiverobj,'receiver':receiver,'receiverform':receiverform,'update':update,'form':form,'cart':cart}
    return render(request,template_name,context)



def cart(request):
    if  request.user.is_authenticated:
        if request.user.is_seller :
            return redirect('homeapp:address') 
    cartdisply=True
    cart,session = session_cart_create(request)
    pds  = cart.products.all()
    # remove all products out of stock from shopper's cart
    for pd in pds:
        #check if there is a product with demanded quantity greater than available stock quantity
       if  pd.quantity > pd.product.instock:
           cart.products.remove(pd)
           cart.save() 
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
        print('size')
        print(sizeid)
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
            if product.instock >= quantity:
                cart.products.add(pobj)
                cart.save()
            else:
                if pobj in cart.products.all():
                    cart.products.remove(pobj)
                    cart.save()
                    #update product tracker object
                    tracker.productincart=False
                    tracker.save() 

        if not pobj:
            # create
            pobj= CostProcessing.objects.create(product=product,color=colorobj,size=sizeobj,quantity=quantity)

            if product.instock >= quantity:
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
def Shopmoredef(request):
    section1,section2,section3 =ShopeMore(request)
    template_name="homeapp/shopemore.html"
    context={'section1':section1,'section2':section2,'section3':section3}
    return render(request,template_name,context)



# product detail 
def ProductDetail(request,slug):
    
    cartdisply=True
    '''
    call the tracker object for this product
    and update the tracker to viewed
    '''
    product =None
    try:
        product =Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
        mstpp,firstp = views.pp_view(request)
        template_name="homeapp/erropage.html"
        return render(request,template_name,context={'tenpds':mstpp})
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
            tracks = Tracker.objects.filter(session=session.id,productdisplay=product,viewed=False).all()
            if tracks:
                #increament product view
                product.views +=1
                product.save()
                for track in tracks:
                    track.viewed=True
                    track.save()
        except ObjectDoesNotExist:
            return redirect('homeapp:home')
        
    # display six  pp_view products to shopper, after they have added a product to cart
    context={'similarfirst':firstsim,'mstpp':mstpp,'simpd':simpd,'cart':cart,'incart':incart,'trending':mstpp,'product':product,'cartdisply':cartdisply}
    template_name="homeapp/productdetail.html"
    return render(request,template_name,context)

def updateproduct(request,slug):
    product=get_object_or_404(Product,slug=slug)
    if request.user.is_admin:
        print('get product update called')
        status = request.GET.get('status')
        if status :
            status=str(status)
            product.status = status
            print(status)
            product.save()
    return redirect('homeapp:productdetail',slug)

# Display used products 
def UsedProduct(request):
    
    cartdisply=True
    cart,session = session_cart_create(request)
    tenpds =UsedProducts(request)
    mstpp,firstpp = views.pp_view(request)
    #check if this page is requested by seller
    if request.user.is_authenticated:
        if request.user.is_seller or request.user.is_admin :
            return redirect('homeapp:address')
    context={'mstpp':mstpp,'cartdisply':cartdisply,'cart':cart.pdcount,'tenpds':tenpds}
    template_name="homeapp/useditems.html"
    return render(request,template_name,context)  

# home page view
def index(request):
    cartdisply=True
    cart,session = session_cart_create(request)
    mstpp,firstpp = views.pp_view(request)
    #check if this page is requested by seller
    if request.user.is_authenticated:
        if request.user.is_seller or request.user.is_admin :
            return redirect('homeapp:address')
    # display 10 random products to visitors
    tenpds = views.FirstTen(request)
    context={'firstpp':firstpp,'mstpp':mstpp,'cartdisply':cartdisply,'cart':cart.pdcount,'tenpds':tenpds}
    template_name='homeapp/index.html'
    return render(request,template_name,context)

# account delivery address:
def AddressBook(request,user):
    cart,session = session_cart_create(request)
    address = None
    form  = None
    update= False
    if not request.user.is_authenticated:
        return HttpResponse('Permission denied')
    if  request.user.is_authenticated:
        if request.user.is_seller and request.user.is_admin:
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
                    return redirect('homeapp:shopperaccount')
        else:
            update=True
            addinst=address.last()
            if addinst.user is None:
                addinst.user= request.user
                addinst.save()
            addresinstance= Address.objects.get(user=request.user)
            form = AddressForm(request.POST or None,instance=addresinstance)
            if request.method=="POST":
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.user=request.user
                    instance.save()
                    return redirect('homeapp:shopperaccount')
    template_name ="homeapp/addressbook.html"
    context={'cart':cart,'address':address,'update':update,'form':form}
    return render(request,template_name,context)




# change password 

def passwordchange(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('permission not granted')

    if  request.user.is_authenticated:
        if request.user.is_admin and request.user.is_seller:
            return HttpResponse('permission not granted')
    error="" 
    cart,session  = session_cart_create(request)
    cartdisply=True
     #retrieve all user viewed products
    trackobjs = Tracker.objects.filter(viewed=True,session=session.id,productincart=False)
    if request.method=="GET": 
        username    = request.GET.get("email")
        password    = request.GET.get("passold")
        newpassword = request.GET.get("passnew")
        if password is not None:
            user = authenticate(request,username=username,password=password)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                logout(request)
                return redirect('homeapp:home')
            if user is None:
                error="wrong password"
                
    context = {'error':error,'cart':cart.pdcount,'trackobjs':trackobjs}
    template_name="homeapp/changepassword.html"
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

# regiser shopper
def shopperRegistration(request):
  
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
        user.buyer= True
        # reference the user to self
        user.me =user
        user.save()
        login(request,user)
        return redirect('homeapp:shopperaccount')
    seller= False
    context = {'form':form,'seller':seller}
    template_name="homeapp/shopperregistration.html"
    return render(request,template_name,context)

def Shopperpannel(request):
    if request.user.is_authenticated:
        if request.user.is_seller or request.user.is_admin:
            return HttpResponse('bad request')
        cart,session  = session_cart_create(request)
        cartdisply=True
        #retrieve all user viewed products
        trackobjs = Tracker.objects.filter(viewed=True,session=session.id,productincart=False)
        template_name="homeapp/shopperaccount.html"
        context={'trackobjs':trackobjs,'cartdisply':cartdisply,'cart':cart.pdcount}
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')


#user address setup for sellers /admin

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
        if request.user.is_admin:
            return redirect('homeapp:useradmin')
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