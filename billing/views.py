from django.shortcuts import render
from homeapp.session import session_cart_create
from billing.models import Billing
from billing.forms import billingForm
from order.orderprocessing import PlaceOrder


def BillingAddress(request):
    cart,session = session_cart_create(request)
    billingobj = Billing.objects.filter(owner=session)
    form   = None
    if not billingobj:
        form   = billingForm(request.POST or None)
    if billingobj:
        billingobj = Billing.objects.get(owner=session)
        form = form   = billingForm(request.POST or None,instance=billingobj)
    if request.method =="POST":
        instance= form.save(commit=False)
        instance.owner = session
        instance.save()
        PlaceOrder(request)
    context={'form':form,'billingobj':billingobj}
    template_name="billing/billing.html"
    return render(request,template_name,context)


# mobile moeny payment info
def PayByMobileMoney(request):
    pass

#visa and master card payment info
def PayByMasterOrVisaCard(request):
    pass
