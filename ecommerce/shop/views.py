from django.contrib.auth import authenticate, login,logout
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.contrib import messages
from django.views import View
from shop.models import Category
# Create your views here.
class Categoryview(View):
    def get(self,request):
        cat=Category.objects.all()
        context={'categories':cat}
        return render(request,'category.html',context)


class Productview(View):
    def get(self,request,i):
        c=Category.objects.get(id=i)
        context={'category':c}
        return render(request,'productview.html',context)

from shop.models import Product
class Productdetail(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request,'detail.html',context)


from shop.forms import Registerform,Loginform
class Register(View):
    def get(self,request):
        form_instance=Registerform()
        context={'form':form_instance}
        return render(request,'register.html',context)
    def post(self,request):
        form_instance=Registerform(request.POST)
        if form_instance.is_valid():
             form_instance.save()
             return redirect('shop:userlogin')
        else:
            return render(request,'register.html',{'form':form_instance})



class Userlogin(View):
    def get(self,request):
        form_instance=Loginform()
        context={'form':form_instance}
        return render(request,'login.html',context)
    def post(self,request):
        form_instance=Loginform(request.POST)
        if form_instance.is_valid():
            u=form_instance.cleaned_data['username']
            p=form_instance.cleaned_data['password']
            user=authenticate(username=u,password=p)
            if user and  user.is_superuser:
                login(request, user)
                return redirect('shop:adminhome')
            elif user and user.is_superuser!=True:
                login(request, user)
                return redirect('shop:category')
            else:
                messages.error(request,"invalid credentials")
                return redirect('shop:userlogin')

class Userlogout(View):
    def get(self,requset):
        logout(requset)
        return redirect('shop:userlogin')


#  admin home
class Adminhome(View):
    def get(self,request):
        return render(request,'adminhome.html')


#category form
from shop.forms import categoryform
class Addcategory(View):
    def get(self,request):
        form_instance=categoryform()
        context={'form':form_instance}
        return render(request,'addcategory.html',context)

    def post(self, request):
        form_instance = categoryform(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:adminhome')
        else:
            return render(request, 'addcategory.html', {'form': form_instance})

#product form
from shop.forms import Productform,Stockform
class Addproduct(View):
    def get(self,request):
        form_instance=Productform()
        context={'form':form_instance}
        return render(request,'addproduct.html',context)
    def post(self, request):
        form_instance = Productform(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:adminhome')
        else:
            return render(request, 'addproduct.html', {'form': form_instance})

class Addstock(View):
    def get(self,request,i):
        s=Product.objects.get(id=i)
        form_instance=Stockform(instance=s)
        context={'form':form_instance}
        return render(request,'addstock.html',context)

    def post(self,request,i):
        s=Product.objects.get(id=i)
        form_instance = Stockform(request.POST,instance=s)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:category')
        else:
            return render(request, 'addstock.html', {'form': form_instance})