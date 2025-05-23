from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from api_logic.models import Subscription, UserSubscription
from api_logic.serializers import UserSubscriptionSerializer
import stripe
import os


stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'test-key')


def subscribe_user(user_id, subscription_id):
    try:
        user = User.objects.get(pk=user_id)
        subscription_plan = Subscription.objects.get(pk=subscription_id)

        if UserSubscription.objects.filter(user=user, subscription=subscription_plan, is_active=True).exists():
            raise ValidationError("User is already subscribed to this plan.")

        stripe_customer = stripe.Customer.create(
            email=user.email,
            name=user.username,
        )

        stripe_product = stripe.Product.create(name=subscription_plan.name)

        stripe_price = stripe.Price.create(
            unit_amount=int(subscription_plan.price * 100),
            currency="usd",
            recurring={"interval": subscription_plan.interval},
            product=stripe_product.id,
        )

        stripe_subscription = stripe.Subscription.create(
            customer=stripe_customer.id,
            items=[{"price": stripe_price.id}],
        )

        user_subscription = UserSubscription.objects.create(
            user=user,
            subscription=subscription_plan,
            stripe_subscription_id=stripe_subscription.id,
            is_active=True,
            current_period_end=timezone.datetime.fromtimestamp(
                stripe_subscription["current_period_end"], tz=timezone.utc),
        )

        serializer = UserSubscriptionSerializer(user_subscription)
        return serializer.data

    except User.DoesNotExist:
        raise ValidationError("User not found.")
    except Subscription.DoesNotExist:
        raise ValidationError("Subscription plan not found.")
    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe error: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Failed to subscribe user: {str(e)}")


def unsubscribe_user(user_id):
    """
    Marks the user's active subscription as inactive (cancels it).
    """
    try:
        user_subscription = UserSubscription.objects.filter(
            user_id=user_id, is_active=True).first()
        if user_subscription:
            user_subscription.is_active = False
            user_subscription.cancelled_at = timezone.now()
            user_subscription.save()
            return True
        return False
    except Exception as e:
        raise ValidationError(f"Failed to unsubscribe user: {str(e)}")


def get_user_subscription(user_id):
    """
    Retrieves the active subscription for a user.
    """
    try:
        user_subscription = UserSubscription.objects.filter(
            user_id=user_id, is_active=True).first()
        if user_subscription:
            serializer = UserSubscriptionSerializer(user_subscription)
            return serializer.data
        return None
    except Exception as e:
        raise ValidationError(f"Failed to get subscription: {str(e)}")


def is_user_subscribed(user_id):
    """
    Checks if the user has an active subscription.
    """
    try:
        return UserSubscription.objects.filter(user_id=user_id, is_active=True).exists()
    except Exception as e:
        raise ValidationError(f"Failed to check subscription: {str(e)}")
