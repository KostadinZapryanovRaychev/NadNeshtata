from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    current_period_end = models.DateTimeField()
    plan_name = models.CharField(max_length=100, null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
