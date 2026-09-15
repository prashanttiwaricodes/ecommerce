from django.db import transaction
from .models import Order,OrderItem
from cart.services import get_cart_total
from cart.models import CartItem

@transaction.atomic

def create_order_from_cart(cart):
    total=get_cart_total(cart)

    order=Order.objects.create(
        user=cart.user,
        total_amount=total,
    )

    for item in cart.items.select_related("product"):
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        CartItem.objects.filter(cart=cart).delete()
        return order
      