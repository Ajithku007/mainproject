from django.shortcuts import render
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
