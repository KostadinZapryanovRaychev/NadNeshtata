from django.contrib.auth.models import User
from rest_framework import serializers
from api_logic.models import Subscription, UserSubscription, Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'date_joined']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'name', 'price', 'interval', 'created_at']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    subscription_id = serializers.PrimaryKeyRelatedField(
        source='subscription', queryset=Subscription.objects.all(), write_only=True
    )

    class Meta:
        model = UserSubscription
        fields = [
            'id', 'user', 'subscription', 'subscription_id', 'stripe_subscription_id',
            'is_active', 'current_period_end', 'cancelled_at', 'created_at', 'updated_at'
        ]


class AuthorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Author
        fields = ['user', 'bio', 'profile_picture']
