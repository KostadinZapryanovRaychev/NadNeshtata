from django.urls import path
from .views import RegisterUserView, UserSubscriptionView

urlpatterns = [
    path('users/', RegisterUserView.as_view(), name="register_user"),
    path('users/<int:user_id>/', RegisterUserView.as_view(), name="get_user"),
    path('users/<int:user_id>/subscribe/',
         UserSubscriptionView.as_view(), name="subscribe_user"),
    path('users/<int:user_id>/unsubscribe/',
         UserSubscriptionView.as_view(), name="unsubscribe_user"),
    path('users/<int:user_id>/subscription/',
         UserSubscriptionView.as_view(), name="get_user_subscription"),

]
