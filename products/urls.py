from django.conf.urls import  url 
from .import views

app_name="product"
urlpatterns=[
      url(r'^product/request/$',views.RequestProduct,name="productrequest"),
    url(r'^products/$',views.myproduct,name="allproducts"),
]