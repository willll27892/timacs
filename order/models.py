from django.db import models
from homeapp.models import Sessionlog
from homeapp.models import CustomUser,Address
from products.models import Cart
from order.orderid import Orderid
from products.models import Product,CostProcessing
from decimal  import Decimal as D


class ReceiversName(models.Model):
    created = models.DateTimeField(auto_now=True, null=True)
    session = models.ForeignKey(Sessionlog,on_delete=models.CASCADE,null=True)
    name    = models.CharField(max_length=200,null=True)
    contact = models.IntegerField(null=True)


# order model
class ProductOrder(models.Model):
    transactioncode = models.CharField(max_length=200,null=True)
    active          = models.BooleanField(default=False)
    paid            = models.BooleanField(default=False)
    receivername    = models.ForeignKey(ReceiversName,on_delete=models.CASCADE,null=True,related_name='receiver')
    authowner       = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    address         = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    cart            = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    buyer           = models.ForeignKey(Sessionlog,on_delete=models.CASCADE,null=True)
    orderid         = models.CharField(max_length=200,null=True)
    created         = models.DateTimeField(auto_now_add=True,null=True)
    updated         = models.DateTimeField(auto_now=True,null=True)
    amount          = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.orderid:
            instance    = self
            firstId     = str("{session}{address}".format(address=self.address.address1,session=self.buyer.id))
            secondId    = str("{address}".format(address=self.address.town))
            orderId     =  Orderid(instance,firstId,secondId)
            # set order id
            self.orderid = orderId
            print('first')
            print(orderId)
        return super(ProductOrder,self).save(*args,**kwargs)


# order status model.
class Orderstatus(models.Model):
    buyer     =models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,related_name="buyers")
    admin     = models.ManyToManyField(CustomUser)
    order     = models.ForeignKey(ProductOrder,on_delete=models.CASCADE,null=True,related_name="status")
    dispatch  = models.BooleanField(default=False)
    shipped   = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    canceled  = models.BooleanField(default=False)
    calls     = models.IntegerField(default=0)
    comments   = models.TextField(null=True)
    def save(self,*args,**kwargs):
        MainOrderUpdate(instance=self)
        return super(Orderstatus,self).save(*args,**kwargs)
    



#product sub order model
# create suborder for products
# suborder stores detail information of each product 
# in placed order. Such as the seller of the product, quantity etc

class SubOrder(models.Model):
    st=(('sold','sold'),('refunded','refunded'),('processing','processing'),('cancelled','cancelled'))
    buyer              = models.ForeignKey(Sessionlog,on_delete=models.CASCADE,null=True)
    seller             = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    product            = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity           = models.IntegerField(null=True)
    amount             = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    productorder       = models.ForeignKey(ProductOrder,on_delete=models.CASCADE,null=True,related_name="suborder")
    productorderid     = models.CharField(max_length=200,null=True)
    created            = models.DateTimeField(auto_now_add=True,null=True)
    updated            = models.DateTimeField(auto_now=True,null=True)
    state              = models.CharField(choices=st,max_length=100,default="processing")
    reason             = models.CharField(max_length=200,null=True)
    orderinfo          = models.ForeignKey(CostProcessing,null=True,on_delete=models.CASCADE)
    def save(self,*args,**kwargs):
    
        return super(SubOrder,self).save(*args,**kwargs)


'''
this signal is called when ever Orderstatus is save,
It updates orders ,suborders and products related to it

'''
def MainOrderUpdate(instance):
    print('singals called')
    '''
    When user order  cancelled
    '''
    cancel = instance.canceled
    '''
    when product has been delivered to shopper
    '''
    delivered = instance.delivered
    if cancel is True:
        orderobj= instance.order
        orderobj.active=False
        orderobj.save()
        orderobj.cart.active=False
        orderobj.cart.save()
       
        # call suborder function
        secondinstance= orderobj
        state="cancelled"
        SubOrderdef(secondinstance,state,instanceorigin=instance)
    """
    if product delivered to buyer
    """
    if delivered is True:
        print('delivered')
        #get the order  object and update it
        orderobj= instance.order
        orderobj.active=False
        orderobj.save()
        #get cart object and update it
        orderobj.cart.active=False
        orderobj.cart.save()
        secondinstance= orderobj
        state="sold"
        #call the suborder function and update it
        SubOrderdef(secondinstance,state,instanceorigin=instance)


# get all suborder related to main product order
# update suborder

def SubOrderdef(instance,state,instanceorigin):
    suborders = SubOrder.objects.filter(productorder=instance)
    if suborders:
        for suborder in suborders:
            suborder.state=state
            suborder.save()
            """
            When ever an ordere has been delivered,
            minus the product quantity ordered from 
            product instock quantity
            """
            if state=="sold":
                product = suborder.product

                '''
                this function is called when ever 
                orderstatus model is save 

                When delivered is true , product in stock is reduced by quantity of products ordered.
                 Meaning after this call, next post calls
                will not reduce  instock quantity.
                '''
                # register the first post save call when product delivered
                # this will return false after the first call
                if instanceorigin.calls ==0:
                    print('first post save call registered when delivered=True')
                    if product.instock > 0:

                        # get the quantity ordered, and minus it from the quantity instock
                        product.instock -= suborder.quantity
                        product.save()
                        #add the initial call by 1 
                        instanceorigin.calls +=1
                        instanceorigin.save()
                else:
                    print('call greater than one')
     
            
    return None  