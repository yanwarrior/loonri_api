from django.contrib.auth.models import User
from django.db import models

from products.models import Product
from utils.models import Timestamp


class Cart(Timestamp):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_users',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_products',
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.product.name

