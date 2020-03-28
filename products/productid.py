import sys
import random
import string  

# method to generate slug
def  Productid(instance,username,productname):
    # take the first five letters of username and product name
    product_name     = ""
    s                = slice(0,3)
    user_name        ="admin"
    if username is not None:
        user_name        = username[s]
    # check if product name has 5 characters
    if len(productname) >= 3:
        product_name     = productname[s]
    else:
        product_name    = product_name
    klass=instance.__class__
    randomvalues =''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(3))
    #generate unique product id
    id_ = "{username}{productname}{random}".format(username=user_name,productname=product_name ,random=randomvalues) 
    id_exist=klass.objects.filter(uniqueid=id_).exists()
    if id_exist:
        """
        if slug exist , call back the function, 
        until a unique slug id generated.
        """
        return Productid(instance,username,productname)
    
    return id_.lower()