from django.urls import path
from .views import RegisterUserView, GetUserView, UserSubscriptionView, LoginUserView
from api_logic.services import webhook

urlpatterns = [
    path('users/', RegisterUserView.as_view(), name="register_user"),
    path('users/login/', LoginUserView.as_view(), name="login_user"),
    path('users/<int:user_id>/', GetUserView.as_view(), name="get_user"),
    path('users/<int:user_id>/subscription/',
         UserSubscriptionView.as_view(), name="user_subscription"),
    path('webhook/stripe/', webhook.stripe_webhook, name='stripe-webhook'),
]
