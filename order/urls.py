from django.conf.urls import url
from .import views

app_name="order"

urlpatterns=[
    url(r'^user/order/(?P<user>.*)/$',views.userorders,name="userorders"),
    url(r'^user/order/place(?P<user>.*)/$',views.placeorder,name="placeorders")
]