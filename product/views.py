from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .models import Product, ProductReview

# صفحه لیست محصولات
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

# صفحه جزئیات محصول
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)  # دریافت محصول با ID مشخص یا نمایش 404
    return render(request, 'product/product_detail.html', {'product': product})

@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        if rating:
            ProductReview.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

    return redirect('product_detail', pk=product.pk)