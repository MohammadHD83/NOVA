from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
    )
# یعنی یه فیلد برای ذخیره شناسه یکتای جهانی (UUID--Universally Unique Identifierرشته ۳۲ کاراکتری)؛

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4, #به‌صورت خودکار UUID می‌سازه(uuid1وuuid3وuuid5وuuid6)
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'   #user.payment_set.all()
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment' #order.payment  
    )

    amount = models.PositiveIntegerField(verbose_name="مبلغ (تومان)")
#یک کد یکتا برای شناسایی موقت یک تراکنش
#Authorityکد مرجع صادرشده از درگاه
#Token شناسه موقت و یکتای تراکنش
#کدی که درگاه برای شناسایی پرداخت می‌دهد
#زرین‌پال → Authority   درگاه‌ها → Token بعضی → Transaction Token
#کدی که درگاه پرداخت به درخواست پرداخت تو می‌ده و میگه: «این تراکنش ثبت شد، با این کد ادامه بده»
    authority = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Authority / Token"
    )

    ref_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Ref ID"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="توضیحات"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} | {self.amount} | {self.status}"

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"
        ordering = ['-created_at']
