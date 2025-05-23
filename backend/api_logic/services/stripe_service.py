import os
import stripe
from rest_framework.exceptions import ValidationError

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'test-key')


def create_customer(user):
    try:
        return stripe.Customer.create(
            email=user.email,
            name=user.username,
        )
    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe error (create_customer): {str(e)}")


def create_product(name):
    try:
        return stripe.Product.create(name=name)
    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe error (create_product): {str(e)}")


def create_price(unit_amount, currency, interval, product_id):
    try:
        return stripe.Price.create(
            unit_amount=int(unit_amount * 100),
            currency=currency,
            recurring={"interval": interval},
            product=product_id,
        )
    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe error (create_price): {str(e)}")


def create_subscription(customer_id, price_id):
    try:
        return stripe.Subscription.create(
            customer=customer_id,
            items=[{"price": price_id}],
            expand=["latest_invoice.payment_intent"]
        )
    except stripe.error.StripeError as e:
        raise ValidationError(f"Stripe error (create_subscription): {str(e)}")
