import os
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.models import User
from api_logic.models import Subscription, UserSubscription

stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'test-key')
endpoint_secret = os.getenv('STRIPE_WEBHOOK_SECRET', 'test-webhook-secret')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        customer_id = session.get('customer')
        subscription_id = session.get('subscription')

        if UserSubscription.objects.filter(stripe_subscription_id=subscription_id).exists():
            return HttpResponse(status=200)

        stripe_subscription = stripe.Subscription.retrieve(subscription_id)

        customer = stripe.Customer.retrieve(customer_id)
        email = customer.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse(status=400)

        product_id = stripe_subscription['items']['data'][0]['price']['product']
        product = stripe.Product.retrieve(product_id)
        subscription_name = product['name']

        try:
            subscription_plan = Subscription.objects.get(
                name=subscription_name)
        except Subscription.DoesNotExist:
            return HttpResponse(status=400)

        UserSubscription.objects.create(
            user=user,
            subscription=subscription_plan,
            stripe_subscription_id=subscription_id,
            is_active=True,
            current_period_end=make_aware(
                datetime.fromtimestamp(
                    stripe_subscription["current_period_end"])
            )
        )

    elif event['type'] == 'invoice.payment_failed':
        pass

    return HttpResponse(status=200)
