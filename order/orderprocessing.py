from order.models import ProductOrder
from homeapp.session import session_cart_create
from billing.models import Billing
from order.models import ReceiversName,Orderstatus,ProductOrder,SubOrder
from homeapp.session import session_cart_create
from homeapp.models import Address
# Create and return order object

def PlaceOrder(request):
    cart,session =session_cart_create(request)
    receivername = ReceiversName.objects.filter(session=session).last()
    address = Address.objects.filter(session=session).last()
    order = ProductOrder.objects.create(receivername=receivername,buyer=session,cart=cart,address=address,amount=cart.total)
    SubOrderCreate(request,order=order,cart=cart,session=session)
    # create status object for placed order 
    Orderstatus.objects.create(order=order)
    return order

# create suborder for products
# suborder stores detail information of each product 
# in placed order. Such as the seller of the product, quantity etc 
def SubOrderCreate(request,order,cart,session):

    #get all products in cart
    products= cart.products.all()
    print(order.id)
    productorder=order
    orderId   = productorder.orderid
    amount = None
    buyer = session
    for product in products:
        pdIncart = product.product
        quantity = product.quantity
        seller   =  product.product.user
        #check if product is on sales
        if product.product.sales > 0 :
             amount   = product.costaftersales
        else :
            amount   = product.cost

        # create suborder for each product in cart
        SubOrder.objects.create(orderinfo=product,product=pdIncart,buyer=buyer,seller=seller,productorderid=orderId,productorder=productorder,quantity=quantity,amount=amount)
    return None 