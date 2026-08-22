from django.contrib import admin
from .models import Product, Category,ProductImage

# Register your models here.



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name","created_at")
    search_fields=("name",)


class ProductImageInline(admin.TabularInline) :
    model=ProductImage
    extra=1   


@admin.register(Product)  
class ProductAdmin(admin.ModelAdmin):
    list_display=(
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "created_at",
    )  

    list_filter=(
        "category",
        "is_active",
    )

    search_fields=(
        "name",
        "description",
    )

    inlines=[ProductImageInline]
