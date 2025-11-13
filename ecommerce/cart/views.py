

from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.utils.decorators import method_decorator
from django.views import View
from pyexpat.errors import messages
from shop.models import Product
from cart.models import Cart
import uuid
import razorpay

from cart.models import Order_items


# Create your views here.
class Addtocart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p) #check weather the product is added to the cart by the user
            c.quantity+=1 #if true increase the quantity
            c.save()
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)  #else create a new record in the cart table
            c.save()
        return redirect('cart:cartview')

class Cartview(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total+=i.product.price * i.quantity
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)



class reduce(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)
            if c.quantity>1:
               c.quantity-=1
               c.save()
            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')


class deletecart(View):
    def get(self,request,i):
        c=Cart.objects.get(id=i,user=request.user)
        c.delete()
        return redirect('cart:cartview')


#-----checkout---
from django.contrib import messages
from cart.forms import Orderform
def checkstock(c):
    for i in c:

        if i.quantity>i.product.stock:
           return  False
    else:
        return True

import random
class Checkout(View):
    def post(self,request):
        form_instance=Orderform(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.product.price*i.quantity
            o.amount=total
            o.save()
            if(o.payment_method=="online"):
                # Razorpay client connection
                client=razorpay.Client(auth=('rzp_test_Re2KSWyKBOYNfG','fq6hlf1J3lQPzFXt5oPCV93F'))  #(auth=('key_id','key_secret'))
                print(client)
                #place order
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request, 'payment.html',context)
            else:
                o.is_ordered = True  # after successful completion of order
                uid=uuid.uuid4().hex[:14]
                id='order_cod'+uid
                o.order_id=id
                o.save()


                # order_items

                order=Order.objects.get(order_id=id)
                for i in c:
                    o = Order_items.objects.create(order=order, product=i.product, quantity=i.quantity)
                    o.save()
                    o.product.stock -= o.quantity
                    o.product.save()

                    # delete
                c.delete()
                return render(request,'payment.html')



    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        stock=checkstock(c)
        if stock:
           form_instance=Orderform()
           context={'form':form_instance}
           return render(request,'checkout.html',context)
        else:
            messages.error(request,"Product is currently unavailable,please try again later")
            return  render(request,'checkout.html')

#payment success
from cart.models import Order
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
@method_decorator(csrf_exempt,name="dispatch")
class Payment_success(View):
    def post(self,request,i):# i represents the username ,to add user to the session again
        u=User.objects.get(username=i)
        login(request,u)
        response=request.POST #after successful payment razorpay send payment details back to the success view as response
        id=response['razorpay_order_id']
        print(id)

        #order
        order=Order.objects.get(order_id=id)
        order.is_ordered=True #after successful completion of order
        order.save()

        #order_items

        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()

            #delete
        c.delete()
        return render(request,'payment_success.html')




#---your orders
class yourorders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'orders.html',context)

