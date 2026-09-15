from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from cart.services import get_cart_total
from .services import create_order_from_cart
from.models import Order

# Create your views here.
@login_required
def checkout(request):
    cart,_=Cart.objects.get_or_create(user=request.user)
    if request.method =="POST":
        order=create_order_from_cart(cart)
        return render(request,"Order/order_success.html",{"order":order},)

    total=get_cart_total(cart)
    return render(request,"Order/checkout.html",{"cart":cart,"total":total,},)


@login_required
def order_list(request):
    orders=Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"Order/order_list.html",{"orders":orders},)



@login_required
def order_detail(request,order_id):
    order=get_object_or_404(Order.objects.prefetch_related("items__product"), id=order_id, user=request.user,)
    return render(request,"Order/order_detail.html",{"order":order},)    

