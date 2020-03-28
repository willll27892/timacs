# this view is to handle product display logics

from products.models import Product
from django.db.models import Q


"""
Query and return products to be displayed 
in home page 
"""

# display  first ten  radom products to a visitor
def  FirstTen(request):
    #get the first 10 random approved products.
    products = Product.objects.filter(status="pending")[:12]
    return products

# popular products
def Popular(request):
    pass 

# display products of similar category

def SimilarPd(request):
    pass

# Suggest Products to user base on user activities

def Suggestion(request):
    pass 

# display promo items

def Promo(request):
    pass