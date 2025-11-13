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
from cart import  views

app_name='cart'
urlpatterns = [
    path('addtocart/<int:i>',views.Addtocart.as_view(),name="addtocart"),
    path('cartview/',views.Cartview.as_view(),name="cartview"),
    path('reduce/<int:i>',views.reduce.as_view(),name="reduce"),
    path('delete/<int:i>', views.deletecart.as_view(), name="deletecart"),
    path('checkout/',views.Checkout.as_view(),name="checkout"),
    path('payment_success/<i>',views.Payment_success.as_view(),name="payment_success"),
    path('orders/',views.yourorders.as_view(),name="orders"),


]
