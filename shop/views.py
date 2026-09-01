from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from product.models import Product
from shop.models import ContactMessage


# --- صفحه اصلی ---
def index(request):
    products = Product.objects.all()[:8]
    return render(request, 'shop/index.html', {'products': products})






def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )

        messages.success(
            request,
            'پیام شما با موفقیت ثبت شد. پاسخ از طریق پنل یا ایمیل اطلاع‌رسانی می‌شود.'
        )
        return redirect('shop:contact')

    return render(request, 'contact.html')