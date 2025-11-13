"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from shop import  views
from django.conf import settings
from django.conf.urls.static import static
app_name='shop'
urlpatterns = [
    path('',views.Categoryview.as_view(),name="category"),
    path('productview/<int:i>',views.Productview.as_view(),name="products"),
    path('detail/<int:i>',views.Productdetail.as_view(),name="productdetail"),
    path('register/',views.Register.as_view(),name="register"),
    path('login/',views.Userlogin.as_view(),name="userlogin"),
    path('adminhome/',views.Adminhome.as_view(),name="adminhome"),
    path('logout/',views.Userlogout.as_view(),name="userlogout"),
    path('addcategory/',views.Addcategory.as_view(),name="addcategory"),
    path('addproduct/',views.Addproduct.as_view(),name="addproduct"),
    path('addstock/<int:i>',views.Addstock.as_view(),name="addstock"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)