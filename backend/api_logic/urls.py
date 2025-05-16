from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path('users/', RegisterUserView.as_view(), name="register_user"),
    path('users/<int:user_id>/', RegisterUserView.as_view(), name="get_user"),
]
