from django.db import models

from django.db import models
from django.conf import settings
from product.models import Product
class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='carts',  
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        if self.user:
            return f"سبد خرید {self.user.username}"
        return f"سبد خرید ناشناس {self.id}"
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity
    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

# Create your models here.
