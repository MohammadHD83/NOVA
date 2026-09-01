from django.contrib import admin
from .models import Payment
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'amount',
        'status',
        'created_at',
        'paid_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('user__phone_number', 'ref_id', 'authority')
    readonly_fields = (
        'id',
        'authority',
        'ref_id',
        'created_at',
        'paid_at'
    )
    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('user',)
        }),
        ('اطلاعات پرداخت', {
            'fields': ('amount', 'status', 'description')
        }),
        ('اطلاعات درگاه', {
            'fields': ('authority', 'ref_id', 'paid_at')
        }),
        ('زمان‌ها', {
            'fields': ('created_at',)
        }),
    )
