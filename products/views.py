from django.shortcuts import render, get_object_or_404,redirect
from .models import Product,Category,Wishlist,ProductReview
from django.contrib.auth.decorators import login_required
from .forms import ProductReviewForm
from django.db.models import Avg
from django.contrib import messages

# Create your views here.
def product_list(request):
    products=Product.objects.filter(is_active=True)
    categories=Category.objects.all()
    query=request.GET.get("q","").strip()

    if query:
        products = products.filter(name__icontains=query)

    category_id=request.GET.get("category","").strip()

    if category_id:
        products = products.filter(category_id=category_id)  


    min_price = request.GET.get("min_price","").strip()
    max_price = request.GET.get("max_price","").strip()

    if min_price:
        products = products.filter(price__gte=min_price)  

    if max_price:
        products = products.filter(price__lte=max_price)  

    sort = request.GET.get("sort","").strip()

    if sort == "price_low":
        products = products.order_by("price")    

    elif sort == "price_high":
        products = products.order_by("-price")   

    elif  sort == "newest":
        products = products.order_by("-created_at")     

    elif   sort == "name":
        products = products.order_by("name")         


    return render(request,"Product/product_list.html",{"products": products,"categories":categories,},)


def product_detail(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True)
    print("PRODUCT:",product)
    reviews=product.reviews.select_related("user").all()
    average_rating=product.reviews.aggregate(average=Avg("rating"))["average"]

    user_review= None
    if request.user.is_authenticated:
        user_review=product.reviews.filter(user=request.user).first()

    return render(request,"Product/product_detail.html",{"product":product,"reviews":reviews,"average_rating":average_rating,"user_review":user_review,},)



@login_required
def wishlist_view(request):
    wishlist_items=(Wishlist.objects.filter(user=request.user).select_related("product"))
    return render(request,"Wishlist/wishlist.html",{"wishlist_items":wishlist_items},)

@login_required
def add_to_wishlist(request,product_id):
    product=get_object_or_404(Product,id=product_id,is_active=True,)
    Wishlist.objects.get_or_create(user=request.user,product=product)

    return redirect("products:list")



@login_required
def remove_from_wishlist(request,product_id):
    Wishlist.objects.filter(user=request.user,product_id=product_id,).delete()

    return redirect("products:wishlist")






@login_required
def add_review(request,product_id):
    product=get_object_or_404(
        Product,id=product_id,is_active=True,
    )

    existing_review=ProductReview.objects.filter(product=product,user=request.user,).first()

    if existing_review:
        messages.info(
            request,"you have already reviewed this product",
        )
        return redirect("products:detail",product_id=product.id,)

    if request.method =="POST":
        form=ProductReviewForm(request.POST)

        if form.is_valid():
            review=form.save(commit=False)
            review.product=product
            review.user=request.user
            review.save()

    return redirect("products:detail",product_id=product.id)


@login_required
def edit_review(request,review_id):
    review=get_object_or_404(ProductReview,id=review_id,user=request.user,)

    if request.method =="POST":
        form=ProductReviewForm(request.POST,instance=review)

        if form.is_valid():
            form.save()
            return redirect("products:detail",product_id=review.product.id,)
    else:
        form=ProductReviewForm(instance=review)


    return render(request,"Product/review_edit.html",{"form":form,"review":review,},)



@login_required
def delete_review(request,review_id):
    review=get_object_or_404(ProductReview,id=review_id,user=request.user,
    )
    product_id=review.product.id
    review.delete()

    return redirect("products:detail",product_id=review.product.id,)





