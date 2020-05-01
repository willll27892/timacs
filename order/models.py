from django.db import models
from homeapp.models import Sessionlog
from homeapp.models import CustomUser,Address
from products.models import Cart
from order.orderid import Orderid


# order model
class ProductOrder(models.Model):
    active    = models.BooleanField(default=True)
    authowner = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    address   = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    cart      = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    session   = models.ForeignKey(Sessionlog,on_delete=models.CASCADE,null=True)
    orderid   = models.CharField(max_length=200,null=True)
    created   = models.DateTimeField(auto_now_add=True,null=True)
    updated   = models.DateTimeField(auto_now=True,null=True)
    amount    = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    def save(self,*args,**kwargs):
        if not self.uniqueid:
            instance    = self
            firstId     = str(self.id) + str("{session}{address}".format(address=self.address.address1,session=self.session.id))
            secondId    = str("{address}".format(address=self.address.town))
            orderId     =  Orderid(instance,firstId,secondId)
            # set order id
            self.orderid = orderId
        return super(ProductOrder,self).save(*args,**kwargs)

# order status model.
class Orderstatus(models.Model):
    order     = models.ForeignKey(ProductOrder,on_delete=models.CASCADE,null=True)
    dispatch  = models.BooleanField(default=False)
    shipped   = models.BooleanField(default=False)
    delivered = models.BooleanField(default=True)
    def save(self,*args,**kwargs):
        if self.delivered is True:
            self.order.active=True
            self.order.save()
        return super(Orderstatus,self).save(*args,**kwargs)
