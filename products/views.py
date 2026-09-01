from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def product_list(request):
    products=Product.objects.filter(is_active=True)
    

    return render(request,"Product/product_list.html",{"products": products},)


def product_detail(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True)
    print("PRODUCT:",product)

    return render(request,"Product/product_detail.html",{"product":product},)