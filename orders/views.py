from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from cart.models import Cart, CartItem
from .models import Order, OrderItem, OrderAddress, DiscountCode


@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "سبد خرید شما خالی است")
        return redirect('cart:cart_detail')

    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price()
    )

    # انتقال آیتم‌ها از سبد خرید به سفارش
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    # پاک کردن سبد خرید
    cart.items.all().delete()
    order.save()

    return redirect('order:add_address', order_id=order.id)


@login_required
def add_order_address(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        OrderAddress.objects.create(
            order=order,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
        )
        return redirect('order:apply_discount', order_id=order.id)

    return render(request, 'orders/add_address.html', {'order': order})


@login_required
def apply_discount(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        code = request.POST.get('code')

        try:
            discount = DiscountCode.objects.get(code__iexact=code)
        except DiscountCode.DoesNotExist:
            messages.error(request, "کد تخفیف نامعتبر است")
            return redirect('order:apply_discount', order_id=order.id)

        if not discount.is_valid(order.total_price):
            messages.error(request, "این کد تخفیف قابل استفاده نیست")
            return redirect('order:apply_discount', order_id=order.id)

        discount_amount = discount.calculate_discount(order.total_price)

        order.discount_code = discount
        order.discount_amount = discount_amount
        order.save()

        discount.used_count += 1
        discount.save()

        messages.success(request, "کد تخفیف اعمال شد")
        return redirect('order:order_detail', order_id=order.id)

    return render(request, 'orders/apply_discount.html', {'order': order})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )