from django.contrib import admin
from .models import Order, OrderItem, OrderAddress, DiscountCode


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")

class OrderAddressInline(admin.StackedInline):
    model = OrderAddress
    extra = 0
    readonly_fields = ("full_name", "phone", "city", "address", "postal_code")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "total_price",
        "discount_amount",
        "is_paid",
        "created_at",
    )

    list_filter = (
        "status",
        "is_paid",
        "created_at",
    )

    search_fields = (
        "id",
        "user_username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
    
    inlines = [OrderItemInline, OrderAddressInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

    search_fields = (
        "order_id",
        "product_name",
    )

@admin.register(OrderAddress)
class OrderAddressAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "full_name",
        "phone",
        "city",
        "postal_code",
    )

    search_fields = (
        "full_name",
        "phone",
        "city",
        "product_code",
    )

@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "value",
        "min_order_amount",
        "usage_limit",
        "used_count",
        "is_active",
        "valid_from",
        "valid_to",
    )

    list_filter = (
        "discount_type",
        "is_active",
        "valid_from",
        "valid_to",
    )

    search_fields = (
        "code",
    )