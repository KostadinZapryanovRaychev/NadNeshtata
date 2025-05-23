from django.db import models
from django.contrib.auth.models import User
class Subscription(models.Model):
    name = models.CharField(max_length=100, unique=True, default='Basic Plan')
    price = models.DecimalField(max_digits=8, decimal_places=2 , default='20.00')
    interval = models.CharField(max_length=20, default='month')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    current_period_end = models.DateTimeField()
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'subscription')

    def __str__(self):
        return f"{self.user.username} - {self.subscription.name}"
