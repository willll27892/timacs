from django.conf.urls import url 
from django.urls import path
from .import views

app_name="homeapp"

urlpatterns=[
    #home page url
    url(r'^$',views.index,name="home"),
    url(r'^login/$',views.Login,name="login"),
    url(r'^urlredirect/$',views.UrlRedirect,name="homeredirect"),
    url(r'^user_pannel_admin/$',views.UserAdmin,name="useradmin"),
    url(r'^logout/$',views.Logout,name="logout"),
    url(r'^membership/$',views.membership,name="members"),
    url(r'^address_setup_/$',views.address_set_up,name="address"),
    url(r'^seller_registration/$',views.register_seller,name="seller")
]