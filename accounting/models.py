from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from acceptances.models import Acceptance
from utils.models import Timestamp


class Profoss(Timestamp):
    purpose = models.CharField(max_length=200, blank=True, null=True)
    acceptance = models.ForeignKey(
        Acceptance,
        related_name='profoss_acceptances',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        related_name='proofoss_users',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    cost_in = models.PositiveIntegerField(default=0)
    cost_out = models.PositiveIntegerField(default=0)
    date = models.DateField(default=now)

    def __str__(self):
        return self.user.username if self.user else 'No username'
