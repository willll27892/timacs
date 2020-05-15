from django.conf.urls import url 
from .import views

app_name="affiliate"

urlpatterns=[

    url(r'^application/$',views.Apply,name="apply"),
]
