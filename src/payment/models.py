# payment/models.py
import uuid

from django.contrib.auth.models import User
from django.db import models


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('stripe', 'Credit/Debit Card (Stripe)'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    payment_id = models.CharField(max_length=200, blank=True, null=True)  # Stripe/PayPal ID
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"{uuid.uuid4().hex.upper()[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_id} - {self.get_method_display()} - {self.status}"
