from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


def register_user(username, password, email):
    """
    Service to register a user.
    """
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username is already taken.")
    
    user = User.objects.create_user(username=username, password=password, email=email)
    return user

def get_user_data(user_id):
    """
    Service to get user data by user ID.
    """
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise ValidationError("User not found.")
    return user