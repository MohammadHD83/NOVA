from django.db import models


class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('new', 'جدید'),
        ('answered', 'پاسخ داده شده'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    admin_reply = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    replied_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"