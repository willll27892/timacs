from django.contrib import admin
from .models import ProductRequest,Tracker,Cart,SubCategory,Category,Product,CostProcessing


admin.site.register(ProductRequest)
admin.site.register(Tracker)
admin.site.register(CostProcessing)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(Cart)
# Register your models here.
