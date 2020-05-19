from django.conf.urls import url 
from django.urls import path
from .import views

app_name="homeapp"
urlpatterns=[
    url(r'^contact/timacs/',views.Contact,name="contact"),
    url(r'^buyer/terms/condition',views.BuyerTerms,name="buyerterms"),
    url(r'^data/privacy',views.userprivacy,name="datapolicies"),
    url(r'^about/timacs/',views.AboutUs,name="aboutus"),
    url(r'^search/return_and_delivery/policies/',views.delivery_and_return_policies,name="returnpolicies"),
    url(r'^search/timacs/',views.inputsearch,name="inputsearch"),
    url(r'^tag/category/product/quick-search/(?P<category>.*)/$',views.quicklinkscat,name="quicklinkscat"),
     url(r'^tag/product/quick-search/(?P<cat>.*)/(?P<subcat>.*)/$',views.quicklinks,name="quicklinks"),
    url(r'^seller/agreement/$',views.selleragreement,name="Sellertermsandcondition"),
    url(r'^shope/more/$',views.Shopmoredef,name="shopemore"),
    #home page url
    url(r'^items/used/$',views.UsedProduct,name="usedItems"),
    url(r'^shopper/user/account/addressbook/(?P<user>.*)/$',views.AddressBook,name="addressbook"),
    url(r'^shopper/user/account/password/change/(?P<user>.*)/$',views.passwordchange,name="passwordchange"),
    url(r'^shopper/user/account$',views.Shopperpannel,name="shopperaccount"),
    url(r'^shopper/$',views.shopperRegistration,name="shopper"),
    url(r'^place_order/$',views.Order,name="order"),
    url(r'^remove/product/cart/$',views.RemoveProduct,name="removeproduct"),
    url(r'^update/cart/$',views.CartUpdate,name="updatecart"),
    url(r'^cart/$',views.cart,name="mycart"),    
    url(r'^cart/(?P<slug>[\w-]+)$',views.AddToCart,name="addtocart"),
    url(r'^product/detail/(?P<slug>[\w-]+)$',views.ProductDetail,name="productdetail"),
    url(r'^product/update/(?P<slug>[\w-]+)$',views.updateproduct,name="updateproduct"),
    url(r'^$',views.index,name="home"),
    url(r'^login/$',views.Login,name="login"),
    url(r'^urlredirect/$',views.UrlRedirect,name="homeredirect"),
    url(r'^user_pannel_admin/$',views.UserAdmin,name="useradmin"),
    url(r'^logout/$',views.Logout,name="logout"),
    url(r'^membership/$',views.membership,name="members"),
    url(r'^address_setup_/$',views.address_set_up,name="address"),
    url(r'^seller_registration/$',views.register_seller,name="seller")
]