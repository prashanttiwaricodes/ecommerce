from django.db import models
from django.conf import settings
from products.models import Product



# Create your models here.
class Order(models.Model):
    STATUS_CHOICES=[
        ("pending","Pending"),
        ("confirmed","Confirmed"),
        ("shipped","Shipped"),
        ("delivered","Delivered"),
        ("cancelled","Cancelled"),
    ]

    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="orders",)
    subtotal_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    discount_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0,)
    coupon=models.ForeignKey("Coupon",on_delete=models.SET_NULL, null=True,blank=True,related_name="orders",)

    total_amount=models.DecimalField(max_digits=10,decimal_places=2,)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="pending",)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items",)
    product=models.ForeignKey(Product,on_delete=models.PROTECT,)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2,)

    def __str__(self):
        return f"{self.product.name}*{self.quantity}"




class Coupon(models.Model):
    DISCOUNT_TYPES=[
        ("percentage","Percentage"),
        ("fixed","Fixed Amount"),
    ]   

    code=models.CharField(
        max_length=50,unique=True,
    ) 
    discount_type=models.CharField(
        max_length=20,choices=DISCOUNT_TYPES,
    )
    discount_value=models.DecimalField(
        max_digits=10,decimal_places=2,
    )
    minimum_order_amount=models.DecimalField(
        max_digits=10,decimal_places=2,default=0,
    )
    is_active=models.BooleanField(default=True)
    expires_at=models.DateTimeField(null=True,blank=True)

    usage_limit=models.PositiveIntegerField(null=True,blank=True)
    used_count=models.PositiveIntegerField(default=0)

    created_at=models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.code

