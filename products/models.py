from django.db import models

from utils.models import Timestamp


class Product(Timestamp):
    product_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


