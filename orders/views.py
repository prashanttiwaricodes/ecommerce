from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart
from cart.services import get_cart_total
from .services import create_order_from_cart, validate_coupon
from.models import Order,Coupon
from django.contrib import messages
from decimal import Decimal, ROUND_HALF_UP

# Create your views here.
@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code","").strip()

        cart,_= Cart.objects.get_or_create(
            user=request.user
        )
        total=get_cart_total(cart)

        coupon,result = validate_coupon(code, total)
        if coupon is None:
            messages.error(request, result)
            return redirect("orders:checkout")

        request.session["coupon_code"] = coupon.code

        messages.success(
            request,
            f"Coupon{coupon.code} applied successfully."
        )
        return redirect("orders:checkout")


















@login_required
def checkout(request):
    cart,_=Cart.objects.get_or_create(user=request.user)
    if request.method =="POST":
        coupon=None
        coupon_code= request.session.get("coupon_code")

        if coupon_code:
            try:
                coupon=Coupon.objects.get(
                    code=coupon_code
                )
            except Coupon.DoesNotExist:
              request.session.pop("coupon_code",None)
        try:
            order=create_order_from_cart(cart,coupon=coupon)

        except ValueError as e:
            messages.error(request, str(e))

            return redirect("orders:checkout") 

        request.session.pop("coupon_code",None)

        return render(request,"Order/order_success.html",{"order":order},) 

    subtotal=get_cart_total(cart)  

    coupon=None
    discount=Decimal("0.00")
    final_total=subtotal

    coupon_code=request.session.get("coupon_code")

    if coupon_code:
        coupon, result= validate_coupon(
            coupon_code,
            subtotal,
        )

        if coupon is None:
            messages.error(request, result)
            request.session.pop("coupon_code", None)

        else:
            discount= result
            final_total= (
                subtotal - discount
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )   


    return render(request,"Order/checkout.html",{"cart":cart,"subtotal":subtotal,"coupon":coupon,"discount":discount,"final_total":final_total},)   
   


@login_required
def order_list(request):
    orders=Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request,"Order/order_list.html",{"orders":orders},)



@login_required
def order_detail(request,order_id):
    order=get_object_or_404(Order.objects.prefetch_related("items__product"), id=order_id, user=request.user,)
    return render(request,"Order/order_detail.html",{"order":order},)    

