from sqlite3 import IntegrityError
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from backend.api_logic.serializers import UserSerializer


def register_user(username, password, email, first_name, last_name):
    """
    Registers a new user with the provided username, password, and email.

    This function checks if the given username already exists in the system. 
    If the username is available, it creates a new user using Django's built-in 
    user model (`User`) and returns the created user instance.

    Args:
        username (str): The desired username for the new user.
        password (str): The password for the new user account.
        email (str): The email address of the new user.

    Returns:
        User: The newly created user object.

    Raises:
        ValidationError: If a user with the provided username already exists.
    """
    try:
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email, is_active=False)
        user.set_password(password)
        user.save()
        return user
    except IntegrityError:
        raise ValidationError("Username is already taken.")
    except Exception as e:
        raise ValidationError(f"Failed to register user: {str(e)}")


def get_user_data(user_id):
    """
    Retrieves user data for a given user ID.

    This function attempts to fetch a user from the database using the provided 
    user ID. If the user exists, their user object is returned. If no user is 
    found with the given ID, a ValidationError is raised.

    Args:
        user_id (int): The unique identifier of the user to retrieve.

    Returns:
        User: The user object corresponding to the provided ID.

    Raises:
        ValidationError: If no user with the given ID exists or other retrieval error occurs.
    """
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return serializer.data
    except User.DoesNotExist:
        raise ValidationError("User not found.")
    except Exception as e:
        raise ValidationError(f"Failed to retrieve user: {str(e)}")
