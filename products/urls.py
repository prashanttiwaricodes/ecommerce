from django.urls import path
from . import views

app_name="products"

urlpatterns=[
    path("",views.product_list, name="list"),
    path("wishlist/",views.wishlist_view,name="wishlist"),
    path("wishlist/add/<int:product_id>/",views.add_to_wishlist,name="wishlist_add",),
     path("wishlist/remove/<int:product_id>/",views.remove_from_wishlist,name="wishlist_remove",),
    path("<int:product_id>/", views.product_detail, name="detail"),
]