from django.urls import path
from . import views
app_name="orders"
urlpatterns=[
    path("",views.order_list,name="list"),
    path("<int:order_id>/",views.order_detail,name="detail"),
    path("checkout/apply-coupon/", views.apply_coupon, name="apply_coupon",),
    path("checkout/",views.checkout,name="checkout"),
]