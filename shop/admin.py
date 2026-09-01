from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')

    fieldsets = (
        ('اطلاعات کاربر', {
            'fields': ('name', 'email', 'message', 'created_at')
        }),
        ('پاسخ ادمین', {
            'fields': ('admin_reply', 'status', 'replied_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.admin_reply and obj.status != 'answered':
            obj.status = 'answered'
        super().save_model(request, obj, form, change)