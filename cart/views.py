
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from product.models import Product
from .models import Cart, CartItem

@login_required
def get_cart(request):
    # اگر برای کاربر لاگین‌شده سبد خرید وجود ندارد، یکی بساز
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart


@login_required
def add_to_cart(request, pk):
    cart = get_cart(request)
    product = get_object_or_404(Product, id=pk)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_cart(request)
    item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if item:
        item.delete()
    return redirect('cart')

@login_required
def cart_detail(request):
    cart = get_cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

# Create your views here.
