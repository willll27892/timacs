from django.shortcuts import  get_object_or_404, render,redirect,HttpResponse
from homeapp.models import Membership,Address
#creating user try period
from homeapp import logics 
from products.forms import ProductSizefm,Productform,Productcolors
from django.http import JsonResponse
from products.models import Product,ProductSize,ProductColor
from products.models import CostProcessing,Product,ProductSize,ProductColor,Tracker
from homeapp.session import session_cart_create
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from productsdisplay import views
from homeapp.activitytracker import CheckIfProductNotIncart,Activity_function,ProductInCart
from order.models import ProductOrder,Orderstatus,SubOrder
from homeapp.models import CustomUser,SellerID
#when user clicks product colors

def ColorClick(request,slug,colorname,idn):
    
    cartdisply=True
    mstpp = None
    print(idn)
    product = get_object_or_404(Product,slug=slug)
    added   = ProductInCart(request,product)
    color   =  get_object_or_404(ProductColor,id=idn)
    firstsim,simpd=views.SimilarPd(request,productobj=product)
    mstpp,firstp = views.pp_view(request)
    if product:
        cart,session = session_cart_create(request)
        try:
            #update tracker object for this product
            track = Tracker.objects.filter(productdisplay=product).first()
            if track:
                
                track.viewed=True
                track.save()
        except ObjectDoesNotExist:
            return redirect('homeapp:home')
    
    
        
    template_name="homeapp/color.html"
    context ={'simpd':simpd,'similarfirst':firstsim,'cart':cart.pdcount,'cartdisply':cartdisply,'trending':mstpp,'added':added,'color':color,'product':product}
    return render(request,template_name,context)

# seller admin pannel
def verificationCheck(request):
    verified=False
    try:
        check = SellerID.objects.get(user=request.user)
        verified= check.verified
    except ObjectDoesNotExist:
        check= SellerID.objects.create(user=request.user)
        verified = check.verified
    return verified, check




def sellerpannel(request):

    #function call which checks user status
    logics.Userstatus()

    accountstate=None
    if request.user.is_authenticated:
        user=request.user
        if user.is_buyer:
            return redirect('homeapp:home')
       
        if request.user.is_seller:
            #function call which checks and create user try period
            accountstate=logics.create_try(user)
            # call the url redirect function 
            # that will do checks and redirect user base on their state
            membership_obj = Membership.objects.filter(user=request.user).first()
            address_obj    = Address.objects.filter(user=request.user).first()
            # check if seller has setup membership or address
            #if one not setup, user redirect to homeredirect for url checkup
            if not membership_obj or not address_obj:
                return redirect('homeapp:homeredirect')
    else:
        return redirect('homeapp:homeredirect')
    verified,check =verificationCheck(request)
    if request.user.is_admin:
        verified=True
    productform= Productform(request.POST or None,request.FILES or None)
    template_name = "adminone/pannel.html"
    context={'verified':verified,'accountstate':accountstate,'productform':productform}
    return render(request,template_name,context)


def deleteproduct(request,slug):
    if request.user.is_admin:
        obj = get_object_or_404(Product,slug=slug)
        obj.delete()
        return redirect('pannel:pending',user=request.user.slug)
    else:
        return HttpResponse('bad request')

# submit product post 

def productpost(request):
    #check if user is authenticated
    if request.user.is_authenticated:
        if request.user.is_buyer:
            return redirect('homeapp:home')
        productform= Productform(request.POST or None,request.FILES or None)
        data={}
        if request.is_ajax():
            print('post called')
            if productform.is_valid():
                print('valid')
                
                instance      = productform.save(commit=False)
                instance.user = request.user
                instance.save()
                data={}
                print('posted')
 
        return JsonResponse(data)


# display all seller posted products

def  Post(request,user):
    if request.user.is_authenticated:
    
        if request.user.is_buyer:
            return redirect('homeapp:home')
        post = None
        if  request.user.is_seller:
            # query all user posted products    
            post = Product.objects.filter(user=request.user).all().order_by('-created')
        if request.user.is_admin:
             post = Product.objects.all().order_by('-created')
        context={"posts":post}
        template_name="adminone/posted.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')


# display all pending products

def Pending(request,user):
    if request.user.is_authenticated:
        if request.user.is_buyer:
            return redirect('homeapp:home')
        pending = None

        if request.user.is_seller:
            pending = Product.objects.filter(Q(user=request.user) & Q(status="pending")).all().order_by('-created')
        if request.user.is_admin:
            pending = Product.objects.filter( Q(status="pending")).all().order_by('-created')
        context={'pending':pending}
        template_name="adminone/pending.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')
                

def Approved(request,user):
    if request.user.is_authenticated:
        if request.user.is_buyer:
            return redirect('homeapp:home')
        app= None
        if request.user.is_seller:
            app = Product.objects.filter(Q(user=request.user) & Q(status="approved")).all().order_by('-created')
        if request.user.is_admin:
            app = Product.objects.filter(Q(status="approved")).all().order_by('-created')

        context={'app':app}
        template_name="adminone/approved.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')

# for sellers to add colors to their product
def Addcolor(request,user,slug):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    if request.user.is_seller or request.user.is_admin:
        product = get_object_or_404(Product,slug=slug)
        form    = Productcolors(request.POST or None, request.FILES or None)
        if request.method=="POST":
            if form.is_valid:
                instance= form.save(commit=False)
                instance.slug = product.slug
                instance.save()
                product.pdcolor.add(instance)
                return redirect ('pannel:addcolors',user=user,slug=product.slug)
        context={'product':product,'form':form}
        template_name="adminone/addcolor.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')
# for sellers to sizes to their product
def Addsize(request,user,slug):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    product = get_object_or_404(Product,slug=slug)
    form    = ProductSizefm(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid:
            instance= form.save(commit=False)
            instance.user        = request.user
            instance.save()
            product.availableseizes.add(instance)
            return redirect ('pannel:addsizes',user=user,slug=product.slug)
    context={'product':product,'form':form}
    template_name="adminone/addsizes.html"

    return render(request,template_name,context)

# remove product colors
def Removecolor(request,user,slug):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    product = get_object_or_404(Product,slug=slug)
    color   = request.GET.get('id')
    sizeobj = ProductColor.objects.get(id=color)
    product.pdcolor.remove(sizeobj)
    return redirect ('pannel:addcolors',user=user,slug=product.slug)

# remove product sizes
def Removesize(request,user,slug):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    product = get_object_or_404(Product,slug=slug)
    size   = request.GET.get('id')
    sizeobj = ProductSize.objects.get(id=size)
    product.availableseizes.remove(sizeobj)
    return redirect ('pannel:addsizes',user=user,slug=product.slug)

# display all orders related to seller 

def DisplayOrders(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    if request.user.is_seller:
        orders=SubOrder.objects.filter(seller=request.user).order_by('-created')
    if request.user.is_admin:
        orders=ProductOrder.objects.all().order_by('-created')
    context={'orders':orders}
    template_name="adminone/orders.html"
    return render(request,template_name,context) 





def subordersearchSold(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    search = request.GET.get('q')
    searhsold=True
    getseller=None
    print(search)
    if search:
        search=str(search)
    
    if request.user.is_seller:
        orders=SubOrder.objects.filter(product__productname=search,seller=request.user,state="sold").order_by('-created')
        
    if request.user.is_admin:
        # get the search seller
        
        if search:
            try:
                getseller = CustomUser.objects.get(email=search)
            except ObjectDoesNotExist:
                getseller= None
        orders=SubOrder.objects.filter(seller=getseller,state="sold").order_by('-created')
    funds=0
    for order in orders:
        funds += order.amount
    context={'funds':funds,'getseller':search,'searhsold':searhsold,'orders':orders}
    template_name="adminone/delivered.html"
    return render(request,template_name,context)



def SearchOrders(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    search = request.GET.get('q')
    if search:
        search=str(search)
    if request.user.is_seller:
        orders=SubOrder.objects.filter(seller=request.user,orderid=search)
    if request.user.is_admin:
        orders=ProductOrder.objects.filter(orderid=search).order_by('-created')
    context={'orders':orders}
    template_name="adminone/searchorders.html"
    return render(request,template_name,context)      

def DeliveredProducts(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    if request.user.is_seller:
        orders=SubOrder.objects.filter(seller=request.user,state="sold").order_by('-created')
    if request.user.is_admin:
        orders=SubOrder.objects.filter(state="sold").order_by('-created')
    context={'orders':orders}
    template_name="adminone/delivered.html"
    return render(request,template_name,context) 




def RefundedProducts(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    if request.user.is_seller:
        orders=SubOrder.objects.filter(seller=request.user,state="refunded").order_by('-created')
    if request.user.is_admin:
        orders=SubOrder.objects.filter(state="refunded").order_by('-created')
    context={'orders':orders}
    template_name="adminone/refunded.html"
    return render(request,template_name,context)

def Searchrefunds(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    orders = None
    search = request.GET.get('q')
    print(search)
    if search:
        search=str(search)
        print(search)
    #get the seller's object to be search
    try:
        getseller = CustomUser.objects.get(email=search)
    except ObjectDoesNotExist:
        getseller= None
    print(getseller)
    if getseller:
        getseller=CustomUser.objects.get(email=search)
        print(getseller)
    if request.user.is_seller:
        orders=SubOrder.objects.filter(productorderid=search,seller=request.user,state="sold").order_by('-created')
    if request.user.is_admin:
        orders=SubOrder.objects.filter(seller=getseller,state="sold").order_by('-created')
    context={'orders':orders}
    template_name="adminone/refunded.html"
    return render(request,template_name,context)

def Funds(request,user):
    if not request.user.is_authenticated:
        return HttpResponse('bad request')
    if request.user.is_buyer:
        return redirect('homeapp:home')
    funds = 0
    refunds = 0
    orders = None
    if request.user.is_seller:
        refundobj=SubOrder.objects.filter(seller=request.user,state="refunded").order_by('-created')
        orders=SubOrder.objects.filter(seller=request.user,state="sold").order_by('-created')
    if request.user.is_admin:
        refundobj=SubOrder.objects.filter(state="refunded").order_by('-created')
        orders=SubOrder.objects.filter(state="sold").order_by('-created')
    for order in orders:
        funds += order.amount
    for reforeder in refundobj:
        refunds += reforeder.amount
    context={'orders':orders,'fund':funds,'refund':refunds}
    template_name="adminone/funds.html"
    return render(request,template_name,context)
    
