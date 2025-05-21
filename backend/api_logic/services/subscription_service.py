from rest_framework.exceptions import ValidationError
from api_logic.models import Subscription
from api_logic.serializers import SubscriptionSerializer


def subscribe_user(user_id, plan_id):
    """
    Subscribes a user to a given plan.

    Args:
        user_id (int): The ID of the user to subscribe.
        plan_id (int): The ID of the plan to subscribe to.

    Returns:
        dict: Serialized subscription data.

    Raises:
        ValidationError: If the subscription fails.
    """
    try:
        subscription = Subscription.objects.create(user_id=user_id, plan_id=plan_id)
        serializer = SubscriptionSerializer(subscription)
        return serializer.data
    except Exception as e:
        raise ValidationError(f"Failed to subscribe user: {str(e)}")


def unsubscribe_user(user_id):
    """
    Unsubscribes a user by removing their subscription.

    Args:
        user_id (int): The ID of the user to unsubscribe.

    Returns:
        bool: True if successfully unsubscribed, False if no subscription was found.
    """
    try:
        subscription = Subscription.objects.filter(user_id=user_id).first()
        if subscription:
            subscription.delete()
            return True
        return False
    except Exception as e:
        raise ValidationError(f"Failed to unsubscribe user: {str(e)}")


def get_user_subscription(user_id):
    """
    Retrieves the subscription of a user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Serialized subscription data or None.

    Raises:
        ValidationError: If retrieval fails.
    """
    try:
        subscription = Subscription.objects.filter(user_id=user_id).first()
        if subscription:
            serializer = SubscriptionSerializer(subscription)
            return serializer.data
        return None
    except Exception as e:
        raise ValidationError(f"Failed to get subscription: {str(e)}")


def is_user_subscribed(user_id):
    """
    Checks if a user is subscribed to any plan.

    Args:
        user_id (int): The ID of the user.

    Returns:
        bool: True if subscribed, False otherwise.

    Raises:
        ValidationError: If check fails.
    """
    try:
        return Subscription.objects.filter(user_id=user_id).exists()
    except Exception as e:
        raise ValidationError(f"Failed to check subscription: {str(e)}")
