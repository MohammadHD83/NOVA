from django.contrib import admin

from .models import Cart , CartItem
# admin.site.register([Cart,CartItem])

#TabularInline

class CartItemInline(admin.TabularInline):  # or admin.StackedInline
    model = CartItem
    extra = 1  # Number of empty image forms to display


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)
    inlines = [CartItemInline]
# Register your models here.
