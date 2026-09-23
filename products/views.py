from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Category,Wishlist
from django.contrib.auth.decorators import login_required

# Create your views here.
def product_list(request):
    products=Product.objects.filter(is_active=True)
    categories=Category.objects.all()
    query=request.GET.get("q","").strip()

    if query:
        products = products.filter(name__icontains=query)

    category_id=request.GET.get("category","").strip()

    if category_id:
        products = products.filter(category_id=category_id)  


    min_price = request.GET.get("min_price","").strip()
    max_price = request.GET.get("max_price","").strip()

    if min_price:
        products = products.filter(price__gte=min_price)  

    if max_price:
        products = products.filter(price__lte=max_price)  

    sort = request.GET.get("sort","").strip()

    if sort == "price_low":
        products = products.order_by("price")    

    elif sort == "price_high":
        products = products.order_by("-price")   

    elif  sort == "newest":
        products = products.order_by("-created_at")     

    elif   sort == "name":
        products = products.order_by("name")         


    return render(request,"Product/product_list.html",{"products": products,"categories":categories,},)


def product_detail(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True)
    print("PRODUCT:",product)

    return render(request,"Product/product_detail.html",{"product":product},)



@login_required
def wishlist_view(request):
    wishlist_items=(Wishlist.objects.filter(user=request.user).select_related("product"))
    return render(request,"Wishlist/wishlist.html",{"wishlist_items":wishlist_items},)

@login_required
def add_to_wishlist(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True,)
    Wishlist.objects.get_or_create(user=request.user,product=product)

    return redirect("products:list")



@login_required
def remove_from_wishlist(request,product_id):
    Wishlist.objects.filter(user=request.user,product_id=product_id,).delete()

    return redirect("products:wishlist")