from django.conf.urls import  url 
from .import views

app_name="pannel"

urlpatterns=[
    url(r'^romove/product/color/(?P<slug>[\w-]+)/(?P<colorname>.*)/(?P<idn>[0-9]+)/$',views.ColorClick,name="colorclicked"),
    url(r'^romove/product/sizes/(?P<slug>[\w-]+)$',views.Removesize,name="removesize"),
    url(r'^remove/product/colors/(?P<slug>[\w-]+)$',views.Removecolor,name="removecolor"),
    url(r'^add/product/sizes/(?P<slug>[\w-]+)$',views.Addsize,name="addsizes"),
    url(r'^add/product/colors/(?P<slug>[\w-]+)$',views.Addcolor,name="addcolors"),
    url(r'^seller/$',views.sellerpannel,name="userpannel"),
    # post product
    url(r'^productpost/$',views.productpost,name="ppost"),
    url(r'^seller/submitted/products/$',views.Post,name="posted"),
    url(r'^seller/pending/products/$',views.Pending,name="pending"),
    url(r'^seller/post/approved/products/$',views.Approved,name="app"),
]