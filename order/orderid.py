import sys
import random
import string  

# method to generate slug
def  Orderid(instance,firstId,secondId):

    s                = slice(0,5)
    if firstId is not None:
        if len(firstId) >= 5:
            firstId= firstId[s]

    if secondId is not None:
        if len(secondId) >=5:
            secondId=secondId[4]
    klass=instance.__class__
    randomvalues =''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(3))
    #generate unique product id
    id_ = "{username}{productname}{random}".format(username=firstId,productname=secondId ,random=randomvalues) 
    id_exist=klass.objects.filter(orderid=id_).exists()
    if id_exist:
        """
        if slug exist , call back the function, 
        until a unique slug id generated.
        """
        return Orderid(instance,firstId,secondId)
    
    return id_.lower()