from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from .services import(add_to_cart,remove_from_cart,update_cart_quantity,)

# Create your views here.
@login_required
def cart_detail(request):
    cart,_=Cart.objects.get_or_create(user=request.user)

    return render(request,"Cart/cart_detail.html",{"cart":cart},)

@login_required
def add_product_to_cart(request,product_id):
    if request.method=="POST":
        add_to_cart(request.user,product_id,)

        return redirect("cart:detail")



@login_required
def update_cart(request,product_id):
    if request.method=="POST":
        quantity=int(request.POST.get("quantity",1))

        update_cart_quantity(request.user,product_id,quantity)   
        return redirect("cart:detail") 


@login_required
def remove_product_from_cart(request,product_id) :
    if request.method=="POST":
        remove_from_cart(request.user,product_id)   
        return redirect("cart:detail")
