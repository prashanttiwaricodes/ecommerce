from django.db import transaction
from .models import Order,OrderItem,Coupon
from cart.services import get_cart_total
from cart.models import CartItem
from products.models import Product
from decimal import Decimal,ROUND_HALF_UP
from django.utils import timezone

@transaction.atomic

def validate_coupon(code,cart_total):
    if not code:
        return None, "Please enter a coupon code."

    code=code.strip().upper()

    try:
        coupon=Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return None, "Invalid coupon code."

    if not coupon.is_active:
        return None, "This coupon is inactive."

    if coupon.expires_at and coupon.expires_at <= timezone.now():
        return None, "This coupon has expired."

    if (
        coupon.usage_limit is not None and coupon.used_count >= coupon.usage_limit
    ):

        return None, "This coupon has reached its usage limit."

    if cart_total < coupon.minimum_order_amount:
        return (
            None,
            f"Minimum order amount for this coupon is{coupon.minimum_order_amount}."

            f"{coupon.minimum_order_amount}.",
        )
    if coupon.discount_type == "percentage":
        discount=(
            cart_total * coupon.discount_value / Decimal("100")
        )
    else:
        discount=coupon.discount_value
        discount=min(discount, cart_total)

        discount=discount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    return coupon, discount

@transaction.atomic        

def create_order_from_cart(cart, coupon=None):
    subtotal=get_cart_total(cart)

    cart_items=list(
        cart.items.select_related("product")
    )

    for item in cart_items:
        product=Product.objects.select_for_update().get(
            id=item.product_id
        )


        if item.quantity > product.stock:
            raise ValueError(
                f"Not enough stock for {product.name}."

            )

        discount=Decimal("0.00")

        if coupon:
            coupon=Coupon.objects.select_for_update().get(
                id=coupon.id
            )

            validated_coupon, result=validate_coupon(
                coupon.code,
                subtotal,
            )

            if validated_coupon is None:
                raise ValueError(result)

            coupon=validated_coupon
            discount=result

        total = subtotal - discount    

    order=Order.objects.create(
        user=cart.user,
        subtotal_amount=subtotal,
        discount_amount=discount,
        coupon=coupon,
        total_amount=total,
    )

    for item in cart_items:
        product=Product.objects.select_for_update().get(
            id=item.product_id
        )
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

        product.stock -= item.quantity
        product.save(
            update_fields=["stock"]
        )
        CartItem.objects.filter(cart=cart).delete()
        return order
      