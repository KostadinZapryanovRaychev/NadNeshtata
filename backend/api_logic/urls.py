from django.urls import path
from .views import RegisterUserView, GetUserView, UserSubscriptionView

urlpatterns = [
    path('users/', RegisterUserView.as_view(), name="register_user"),
    path('users/<int:user_id>/', GetUserView.as_view(), name="get_user"),
    path('users/<int:user_id>/subscription/', UserSubscriptionView.as_view(), name="user_subscription"),
]