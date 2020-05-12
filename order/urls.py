from django.conf.urls import url
from .import views

app_name="order"

urlpatterns=[
    url(r'^/order/detail(?P<user>.*)/(?P<slug>.*)/$',views.orderdetail,name="orderdetail"),
    url(r'^calcel/order/(?P<user>.*)/$',views.Ordercancel,name="ordercancel"),
    url(r'^orderupdate/(?P<pk>[0-9]+)/$',views.OrderUpdate,name="updateorder"),
    url(r'^user/order/(?P<user>.*)/$',views.userorders,name="userorders"),
    url(r'^user/order/place(?P<user>.*)/$',views.placeorder,name="placeorders")
]