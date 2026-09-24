from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.contrib import messages
from .services import(add_to_cart,remove_from_cart,update_cart_quantity,get_cart_total)

# Create your views here.
@login_required
def cart_detail(request):
    cart,_=Cart.objects.get_or_create(user=request.user)
    total=get_cart_total(cart)

    cart_items=[]

    for item in cart.items.select_related("product"):
        item.available_to_add=max(
            item.product.stock - item.quantity,0,
        )
        cart_items.append(item)

    return render(request,"Cart/cart_detail.html",{"cart":cart,"total":total,"cart_items":cart_items},)

@login_required
def add_product_to_cart(request,product_id):
    if request.method=="POST":
       cart_item=add_to_cart(
           request.user,product_id,
       )

       if cart_item is None:
           messages.error(
               request,"Not enough stock available.",
        )

       return redirect("cart:detail")   



@login_required
def update_cart(request,product_id):
    if request.method=="POST":
        quantity=int(request.POST.get("quantity",1))

        cart_item = update_cart_quantity(
            request.user,product_id,quantity
        )

        if cart_item is None and quantity > 0:
            messages.error(
                request,"Requested quantity is greater than available stock.",
            )


        return redirect("cart:detail")    


@login_required
def remove_product_from_cart(request,product_id) :
    if request.method=="POST":
        remove_from_cart(request.user,product_id)   
        return redirect("cart:detail")
