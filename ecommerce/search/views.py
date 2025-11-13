from django.shortcuts import render
from django.views import  View
from shop.models import Product
from django.db.models import Q
# Create your views here.
class Searchview(View):
    def get(self,request):
        query=request.GET['q']
        if query:
            p=Product.objects.filter(Q(name__icontains=query)|Q(price__icontains=query)|Q(description__icontains=query))
            context={'product':p}
            return render(request,'search.html',context)