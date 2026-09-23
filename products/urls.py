from django.urls import path
from . import views

app_name="products"

urlpatterns=[
    path("",views.product_list, name="list"),
    path("wishlist/",views.wishlist_view,name="wishlist"),
    path("wishlist/add/<int:product_id>/",views.add_to_wishlist,name="wishlist_add",),
    path("wishlist/remove/<int:product_id>/",views.remove_from_wishlist,name="wishlist_remove",),
    path("reviews/add/<int:product_id>/",views.add_review,name="review_add",),
    path("reviews/edit/<int:review_id>/",views.edit_review,name="review_edit",),
    path("reviews/delete/<int:review_id>/",views.delete_review,name="review_delete",),
    path("<int:product_id>/", views.product_detail, name="detail"),
]