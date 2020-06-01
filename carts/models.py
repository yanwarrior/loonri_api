from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    class Meta:
        unique_together = ('user', 'product',)

#
# class CartAccumulation(Timestamp):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cartaccumulation_user')
#     total = models.PositiveIntegerField(default=0)
#     items = models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return self.user.username
#
#
# @receiver(post_save, sender=Cart)
# def change_cart(sender, instance: Cart, created, **kwargs):
#     obj, created = CartAccumulation.objects.get_or_create(user=instance.user)
#
#     obj.items += 1
#     obj.total += (instance.product.price * instance.quantity)
#     obj.save()
#


