
from django.urls import path
from .views import RegisterUserView, get_user_view

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register_user"),
    path('user/<int:user_id>/', get_user_view, name="get_user"),
]
