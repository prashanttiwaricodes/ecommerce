from django.db import transaction
from .models import Cart,CartItem
from products.models import Product

@transaction.atomic
def add_to_cart(user,product_id,quantity=1):
    product=Product.objects.get(id=product_id,is_active=True,)
    cart,_ = Cart.objects.get_or_create(user=user)
    cart_item, created=CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity":quantity},
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save(update_fields=["quantity","updated_at"])

        return cart_item


def update_cart_quantity(user,product_id,quantity):
    cart=Cart.objects.get(user=user)  
    cart_item=CartItem.objects.get(
        cart=cart,
        product_id=product_id,
    )  
    if quantity <= 0:
        cart_item.delete()
        return None
    
    cart_item.quantity=quantity
    cart_item.save(update_fields=["quantity","updated_at"])
    return cart_item


def remove_from_cart(user,product_id):
    cart=Cart.objects.get(user=user)

    cart_item=CartItem.objects.get(
        cart=cart,
        product_id=product_id,
                                   
    )
    cart_item.delete()