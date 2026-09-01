from django.db import models
from django.conf import settings
from django.utils import timezone
from product.models import Product
class DiscountCode(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        ('percent', 'درصدی'),
        ('fixed', 'مبلغ ثابت'),
    )
    code = models.CharField(max_length=50, unique=True)

    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES
    )

    value = models.PositiveIntegerField(
        help_text="درصد یا مبلغ تخفیف"
    )

    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="حداکثر مبلغ تخفیف (برای درصدی)"
    )

    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="حداقل مبلغ سفارش"
    )

    is_active = models.BooleanField(default=True)

    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="حداکثر تعداد استفاده"
    )

    used_count = models.PositiveIntegerField(default=0)

    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self, order_total):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from > now or self.valid_to < now:
            return False
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False
        if order_total < self.min_order_amount:
            return False
        return True

    def calculate_discount(self, order_total):
        if self.discount_type == 'percent':
            discount = (self.value / 100) * order_total
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
            return discount
        return min(self.value, order_total)

    def __str__(self):
        return self.code




class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('processing', 'در حال پردازش'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
        ('canceled', 'لغو شده'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    discount_code = models.ForeignKey(
        DiscountCode,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    is_paid = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def get_final_price(self):
        return self.total_price - self.discount_amount

    def __str__(self):
        return f"Order #{self.id} - {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="قیمت محصول در زمان ثبت سفارش"
    )

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
    
class OrderAddress(models.Model):
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='address'
    )

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.TextField()
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
