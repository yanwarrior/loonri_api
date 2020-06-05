from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from carts.models import Cart
from products.models import Product
from utils.models import Timestamp


class Acceptance(Timestamp):
    STATUS_WASHED = 'WASHED'
    STATUS_COMPLETED = 'COMPLETED'
    STATUS_TAKED = 'TAKED'
    STATUS_CHOICES = (
        (STATUS_WASHED, 'Washed'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_TAKED, 'Taked'),
    )

    acceptance_number = models.CharField(max_length=20, unique=True)
    acceptance_date = models.DateField(default=now)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='acceptance_users',
        blank=True,
        null=True
    )
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_phone = models.CharField(max_length=20)
    total = models.PositiveIntegerField(default=0)
    down_payment = models.PositiveIntegerField(default=0)
    residual = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_WASHED)

    def __str__(self):
        return self.acceptance_number


class Item(Timestamp):
    acceptance = models.ForeignKey(
        Acceptance,
        on_delete=models.CASCADE,
        related_name='item_acceptances'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='item_products',
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=20)
    price = models.PositiveIntegerField(default=0)
    sub_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.product.product_number


