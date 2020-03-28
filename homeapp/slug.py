import sys
import random
import string  
from django.utils.text import slugify

# method to generate slug
def  Generate_slug(instance,slug):
    s            = slice(0,40)
    slug         = slug[s]
    klass=instance.__class__
    randomvalues =''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(10))
    slugy        = slugify(slug)
    slug_ck = "{slug}-{random}".format(slug=slugy,random=randomvalues) 
    cl_exist=klass.objects.filter(slug=slug_ck).exists()
    if cl_exist:
        """
        if slug exist , call back the function, 
        until a unique slug id generated.
        """
        return Generate_user_slug(instance,slug)
    return slug_ck