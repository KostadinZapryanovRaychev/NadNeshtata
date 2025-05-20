from django.contrib.auth.models import User
from rest_framework import serializers
from api_logic.models import Subscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'stripe_subscription_id', 'is_active',
                  'current_period_end', 'plan_name', 'cancelled_at', 'created_at', 'updated_at']
