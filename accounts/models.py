from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.core.validators import RegexValidator

phone_regex = RegexValidator(
    regex = r"^(?:\+98|98|0)?9\d{9}$",
    message = "شماره موبایل معتبر وارد کنید",
)

# 1. تعریف UserManager سفارشی
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        
        # تنظیمات پیش‌فرض برای کاربر عادی
        extra_fields.setdefault('is_staff', False)
         
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone number and password.
        """
        # این خطوط اطمینان حاصل می‌کنند که is_staff و is_superuser برای سوپر یوزر True باشد
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # در اینجا، ما از متد create_user خودمان استفاده می‌کنیم
        # و phone_number را به عنوان شناسه اصلی پاس می‌دهیم.
        return self.create_user(phone_number, password, **extra_fields)


# 2. استفاده از UserManager سفارشی در مدل User
class User(AbstractUser):
    username = None
    email = None

    phone_number = models.CharField(
        max_length = 11,
        unique = True,
        validators = [phone_regex],
        verbose_name="شماره موبایل"
    )
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = [] # چون USERNAME_FIELD مشخص است، فیلد دیگری اجباری نیست

    # نسبت دادن UserManager سفارشی به مدل User
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number

# کلاس OtpCode شما بدون تغییر باقی می‌ماند
class OtpCode(models.Model):
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"
