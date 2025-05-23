import stripe , os
from rest_framework.exceptions import ValidationError

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'test-key')

def create_stripe_subscription(customer_id, price_id):
    """
    Create a subscription in Stripe for the given customer and price.

    Args:
        customer_id (str): The Stripe customer ID.
        price_id (str): The Stripe price ID (not the plan ID).

    Returns:
        stripe.Subscription object
    """
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            expand=["latest_invoice.payment_intent"]
        )
        return subscription
    except Exception as e:
        raise ValidationError(f"Failed to create Stripe subscription: {str(e)}")
