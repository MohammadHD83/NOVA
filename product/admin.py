from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}  # تولید خودکار slug از نام
    search_fields = ('name',)
    ordering = ('-created_at',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # نمایش یک فیلد خالی اضافه برای افزودن تصویر جدید


class ProductReviewInline(admin.TabularInline):
    model = ProductReview
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    ordering = ('-created_at',)
    inlines = [ProductImageInline, ProductReviewInline]  # نمایش تصاویر و نظرات داخل صفحه محصول


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text')
    search_fields = ('product__name',)
    list_filter = ('product',)


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'comment')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)