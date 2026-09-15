from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from cart.services import get_cart_total
from .services import create_order_from_cart

# Create your views here.
@login_required
def checkout(request):
    cart,_=Cart.objects.get_or_create(user=request.user)
    if request.method =="POST":
        order=create_order_from_cart(cart)
        return render(request,"Order/order_success.html",{"order":order},)

    total=get_cart_total(cart)
    return render(request,"Order/checkout.html",{"cart":cart,"total":total,},)
