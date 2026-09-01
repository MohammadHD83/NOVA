from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='نام دسته‌بندی')
    slug = models.SlugField(max_length=120, unique=True, verbose_name='نامک (Slug)')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, null=True,on_delete=models.CASCADE, related_name='products', verbose_name='دسته‌بندی')
    name = models.CharField(max_length=100, verbose_name='نام محصول')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='تصویر اصلی محصول')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='محصول')
    image = models.ImageField(upload_to='product_images/', verbose_name='تصویر محصول')
    alt_text = models.CharField(max_length=100, blank=True, null=True, verbose_name='توضیح تصویر')

    class Meta:
        verbose_name = 'تصویر محصول'
        verbose_name_plural = 'تصاویر محصولات'

    def __str__(self):
        return f"تصویر {self.product.name}"


class ProductReview(models.Model):
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='محصول')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    rating = models.PositiveIntegerField(verbose_name='امتیاز (۱ تا ۵)')
    comment = models.TextField(blank=True, null=True, verbose_name='نظر')
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed=models.BooleanField(default=False)

    class Meta:
        verbose_name = 'نظر محصول'
        verbose_name_plural = 'نظرات محصولات'
        ordering = ['-created_at']

    def __str__(self):
        return f"نظر {self.user} برای {self.product}"