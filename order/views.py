from django.shortcuts import render,HttpResponse
from .orderprocessing import PlaceOrder
from order.models import Orderstatus
from django.http import JsonResponse
from homeapp.session import session_cart_create
from order.models import ProductOrder,Orderstatus
from django.core.exceptions import ObjectDoesNotExist


# detail order view
def orderdetail(request,user,slug):
    if request.user.is_authenticated:
        if request.user.is_buyer:
            cart,session=session_cart_create(request)
            mainorder=None
            cartdisply=True
            try:
                mainorder= ProductOrder.objects.get(id=slug)
            except ObjectDoesNotExist:
                pass
            
            context={'cartdisply':cartdisply,'cart':cart.pdcount,'mainorder':mainorder}
            template_name="homeapp/orderdetail.html"
            return render(request,template_name,context)
        else:
            return HttpResponse('bad request')
    else:
        return HttpResponse('bad request')



# function to place and return order
def placeorder(request):
    pass

#user cancele order 

def Ordercancel(request,user):
    if request.user.is_authenticated:
        if request.is_ajax:
            print('ajax call')
            orderid = request.GET.get('id')
            status  = None
            order   = None
            if orderid:
                print(orderid)
                orderid = int(orderid)
                try:
                    order  = ProductOrder.objects.get(id=orderid)
                    status = Orderstatus.objects.get(order=order)
                    status.canceled =True
                    print(status.canceled)
                    status.save() 
                except ObjectDoesNotExist:
                    pass 
        return HttpResponse('submited')    

    else:
        return HttpResponse('bad request')

def userorders(request,user):
    if request.user.is_authenticated:
        if request.user.is_buyer:
            cart,session=session_cart_create(request)
            mainorder= ProductOrder.objects.filter(buyer=session).order_by('-created')
            cartdisply=True
            context={'cartdisply':cartdisply,'cart':cart.pdcount,'mainorder':mainorder}
            template_name="homeapp/shopperorder.html"
            return render(request,template_name,context)
        else:
            return HttpResponse('bad request')
    else:
        return HttpResponse('bad request')
#admin upadate order

def OrderUpdate(request,pk):
    print('status update called')
    if request.method=="GET":
        dispatch  = request.GET.get('dispatch')
        shipped   = request.GET.get('shipped')
        delivered = request.GET.get('delivered')
        comment   = request.GET.get('comment')
        cancelled = request.GET.get('cancelled')
        print(comment)
        print(shipped)
        #update card 
        objs     = Orderstatus.objects.filter(id=pk)
        if objs:
            obj =Orderstatus.objects.get(id=pk) 
            print('this object'+ str(obj))
            if request.user.is_admin:
                obj.admin.add(request.user)
                if dispatch:
                    obj.dispatch  = bool(dispatch)
                if shipped:
                    obj.shipped   = bool(shipped)
                if delivered:
                    obj.delivered = bool(delivered)
                obj.comments   = str(comment)
                obj.save()

            if request.user.is_buyer:
                if cancelled :
                    obj.buyer=request.user
                    obj.canceled=bool(cancelled)
                    obj.save()
        data={}
    return JsonResponse(data)
        
