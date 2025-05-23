from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from api_logic.models import Subscription, UserSubscription
from api_logic.serializers import UserSubscriptionSerializer
from .stripe_service import create_customer, create_product, create_price, create_subscription


def subscribe_user(user_id, subscription_id):
    try:
        user = User.objects.filter(pk=user_id).first()
        if not user:
            raise ValidationError("User not found.")
        subscription_plan = Subscription.objects.filter(pk=subscription_id).first()
        if not subscription_plan:
            raise ValidationError("Subscription plan not found.")
        if UserSubscription.objects.filter(user=user, subscription=subscription_plan, is_active=True).exists():
            raise ValidationError("User is already subscribed to this plan.")

        customer = create_customer(user)
        product = create_product(subscription_plan.name)
        price = create_price(subscription_plan.price, "usd", subscription_plan.interval, product.id)
        stripe_sub = create_subscription(customer.id, price.id)

        user_subscription = UserSubscription.objects.create(
            user=user,
            subscription=subscription_plan,
            stripe_subscription_id=stripe_sub.id,
            is_active=True,
            current_period_end=timezone.datetime.fromtimestamp(
                stripe_sub["current_period_end"], tz=timezone.utc
            )
        )
        return UserSubscriptionSerializer(user_subscription).data
    except ValidationError:
        raise
    except Exception as e:
        raise ValidationError(f"Failed to subscribe user: {str(e)}")


def unsubscribe_user(user_id):
    try:
        user_subscription = UserSubscription.objects.filter(user_id=user_id, is_active=True).first()
        if not user_subscription:
            return False
        user_subscription.is_active = False
        user_subscription.cancelled_at = timezone.now()
        user_subscription.save()
        return True
    except Exception as e:
        raise ValidationError(f"Failed to unsubscribe user: {str(e)}")


def get_user_subscription(user_id):
    try:
        user_subscription = UserSubscription.objects.filter(user_id=user_id, is_active=True).first()
        return UserSubscriptionSerializer(user_subscription).data if user_subscription else None
    except Exception as e:
        raise ValidationError(f"Failed to get user subscription: {str(e)}")


def is_user_subscribed(user_id):
    try:
        return UserSubscription.objects.filter(user_id=user_id, is_active=True).exists()
    except Exception as e:
        raise ValidationError(f"Failed to check user subscription: {str(e)}")
