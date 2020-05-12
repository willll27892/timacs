from django.conf.urls import  url 
from .import views

app_name="pannel"

urlpatterns=[
    url(r'^romove/product/color/(?P<slug>[\w-]+)/(?P<colorname>.*)/(?P<idn>[0-9]+)/$',views.ColorClick,name="colorclicked"),
    url(r'^romove/product/sizes/(?P<user>.*)/(?P<slug>[\w-]+)$',views.Removesize,name="removesize"),
    url(r'^remove/product/colors/(?P<user>.*)/(?P<slug>[\w-]+)$',views.Removecolor,name="removecolor"),
    url(r'^add/product/sizes/(?P<user>.*)/(?P<slug>[\w-]+)$',views.Addsize,name="addsizes"),
    url(r'^add/product/colors/(?P<user>.*)/(?P<slug>[\w-]+)$',views.Addcolor,name="addcolors"),
    url(r'^admin/users/dashboard$',views.sellerpannel,name="userpannel"),
    # post product
    url(r'^productpost/$',views.productpost,name="ppost"),
    url(r'^submitted/products/(?P<user>.*)$',views.Post,name="posted"),
    url(r'^pending/products/(?P<user>.*)$',views.Pending,name="pending"),
    url(r'^post/approved/products/(?P<user>.*)$',views.Approved,name="app"),
    url(r'^admin/orders/display/(?P<user>.*)$',views.DisplayOrders,name="orders"),
    url(r'^admin/orders/delivered/(?P<user>.*)$',views.DeliveredProducts,name="delivered"),
    url(r'^admin/refunded/(?P<user>.*)$',views.RefundedProducts,name="refunded"),
    url(r'^admin/funds/(?P<user>.*)$',views.Funds,name="funds"),
    url(r'^search/orders/(?P<user>.*)$',views.SearchOrders,name="searchorder"),
    url(r'^search/sold/(?P<user>.*)$',views.subordersearchSold,name="searchsold"),
    url(r'^search/refund/(?P<user>.*)$',views.Searchrefunds,name="searchrefunds"),
    url(r'^product/delete/(?P<slug>.*)$',views.deleteproduct,name="deleteproduct"),
]