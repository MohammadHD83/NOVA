from django.contrib import admin
from .models import User , OtpCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','phone_number','is_active','is_staff')
    search_fields = ('email','phone_number')
    list_filter = ('is_active','is_staff')
    ordering= ('id',)


@admin.register(OtpCode)    
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('id','phone','code','created_at')
    search_fields= ('phone',)
    ordering = ('-created_at',)