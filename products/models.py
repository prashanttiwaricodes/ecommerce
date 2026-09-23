from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    

class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE,related_name="products")
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)  
    price=models.DecimalField(max_digits=10,decimal_places=2)  
    stock=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def validate_image_size(image):
    max_size= 5 * 1024 * 1024

    if image.size > max_size:
     raise ValidationError("Image size must be less than 5 mb ")

class ProductImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="images")
    image=models.ImageField(upload_to="products/",
    validators=[validate_image_size],)    
    alt_text=models.CharField(max_length=200,blank=True) 
    created_at=models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.product.name} image"  


class Wishlist(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wishlist_items",) 
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="wishlist_items",) 
    created_at=models.DateTimeField(auto_now_add=True)  


    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["user","product"],
                name="unique_user_product_wishlist",
            )
        ]
        ordering=["-created_at"]

    def __str__(self):
        return f"{self.user.email}-{self.product.name}"    




class ProductReview(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews",) 
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="product_reviews",)  
    rating=models.PositiveSmallIntegerField()
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True) 
    updated_at=models.DateTimeField(auto_now=True)


    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=["product","user"],
                name="unique_user_product_review",

            )
        ]
        ordering=["-created_at"]


    def __str__(self):
        return f"{self.product.name}-{self.user.email}({self.rating}/5)"    
        
