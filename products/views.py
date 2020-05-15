from django.shortcuts import render,HttpResponse
from .forms import  Productform,RequestProductForm
from homeapp.session import session_cart_create
from django.http import JsonResponse


# filter used products





# to request a produc
def RequestProduct(request):
    cart,session = session_cart_create(request)
    form =RequestProductForm(request.POST or None)
    if request.is_ajax:
       
        if form.is_valid:
            instance = form.save(commit=False)
            instance.session = session
            instance.save()
    context={'form':form}
    template_name="homeapp/requestform.html"
    return render(request,template_name,context)

# to view more products 
def myproduct(request):
    pass
