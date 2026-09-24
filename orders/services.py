from django.db import transaction
from .models import Order,OrderItem
from cart.services import get_cart_total
from cart.models import CartItem
from products.models import Product

@transaction.atomic

def create_order_from_cart(cart):
    total=get_cart_total(cart)

    cart_items=list(
        cart.items.select_related("product")
    )

    for item in cart_items:
        product=Product.objects.select_for_update().get(
            id=item.product_id
        )


        if item.quantity > product.stock:
            raise ValueError(
                f"Not enought stock for {product.name}."
            )

    order=Order.objects.create(
        user=cart.user,
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
      