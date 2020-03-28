from django.conf.urls import  url 
from .import views

app_name="pannel"

urlpatterns=[
    url(r'^seller/$',views.sellerpannel,name="userpannel"),
    # post product
    url(r'^productpost/$',views.productpost,name="ppost"),
    url(r'^seller/submitted/products/$',views.Post,name="posted"),
    url(r'^seller/pending/products/$',views.Pending,name="pending"),
    url(r'^seller/post/approved/products/$',views.Approved,name="app"),
]