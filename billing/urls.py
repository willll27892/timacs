from django.conf.urls import url
from .import views
app_name="billing"

urlpatterns=[
    url(r'^billing/address/$',views.BillingAddress,name="billingaddress"),
]