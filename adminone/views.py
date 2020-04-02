from django.shortcuts import  get_object_or_404, render,redirect,HttpResponse
from homeapp.models import Membership,Address
from products import logics 
from products.forms import ProductSizefm,Productform,Productcolors
from django.http import JsonResponse
from products.models import Product
from django.db.models import Q


# seller admin pannel

def sellerpannel(request):

    #function call which checks user status
    logics.Userstatus()

    accountstate=None
    if request.user.is_authenticated:
        user=request.user
       
       #function call which checks and create user try period
        accountstate=logics.create_try(user)
        if request.user.is_seller:
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
    productform= Productform(request.POST or None,request.FILES or None)
    template_name = "adminone/pannel.html"
    context={'accountstate':accountstate,'productform':productform}
    return render(request,template_name,context)


# submit product post 

def productpost(request):
    #check if user is authenticated
    if request.user.is_authenticated:
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

def  Post(request):
    if request.user.is_authenticated:
        if not request.user.is_seller:
            return HttpResponse('bad request')
        # query all user posted products    
        post = Product.objects.filter(user=request.user).all().order_by('-created')
        context={"posts":post}
        template_name="adminone/posted.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')


# display all pending products

def Pending(request):
    if request.user.is_authenticated:
        pending = Product.objects.filter(Q(user=request.user) & Q(status="pending")).all().order_by('-created')
        context={'pending':pending}
        template_name="adminone/pending.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')
                

def Approved(request):
    if request.user.is_authenticated:
        app = Product.objects.filter(Q(user=request.user) & Q(status="posted")).all().order_by('-created')
        context={'app':app}
        template_name="adminone/approved.html"
        return render(request,template_name,context)
    else:
        return HttpResponse('bad request')

# for sellers to add colors to their product
def Addcolor(request,slug):
    product = get_object_or_404(Product,slug=slug)
    form    = Productcolors(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid:
            instance= form.save(commit=False)
            instance.productname = product.productname
            instance.location    = product.location
            instance.category    = product.category
            instance.subcategory = product.subcategory
            instance.user        = request.user
            instance.status      = product.status
            instance.state       = product.state
            instance.sales       = product.sales
            instance.brand       = product.brand
            instance.model       = product.model
            instance.descript   = product.descript
            instance.pdprice    = product.pdprice
            instance.sales       = product.sales
            instance.save()
            product.pdcolor.add(instance)
            return redirect ('pannel:addcolors',slug=product.slug)
    context={'product':product,'form':form}
    template_name="adminone/addcolor.html"

    return render(request,template_name,context)

# for sellers to sizes to their product
def Addsize(request,slug):
    product = get_object_or_404(Product,slug=slug)
    form    = ProductSizefm(request.POST or None, request.FILES or None)
    if request.method=="POST":
        if form.is_valid:
            instance= form.save(commit=False)
            instance.user        = request.user
            instance.save()
            product.availableseizes.add(instance)
            return redirect ('pannel:addcolors',slug=product.slug)
    context={'product':product,'form':form}
    template_name="adminone/addsizes.html"

    return render(request,template_name,context)
                


    
