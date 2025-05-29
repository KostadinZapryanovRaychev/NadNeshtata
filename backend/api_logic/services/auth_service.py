from sqlite3 import IntegrityError
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from api_logic.serializers import UserSerializer
from django.contrib.auth import authenticate, login
from knox.models import AuthToken
from api_logic.utils import UserUtils

# TODO = to add confirmation by email and activation of the user account


def register_user(username, password, email, first_name, last_name, request):
    """
    Registers a new user with the provided username, password, and email.

    This function checks if the given username already exists in the system.
    If the username is available, it creates a new user using Django's built-in
    user model (`User`) and returns the created user instance.

    Args:
        username (str): The desired username for the new user.
        password (str): The password for the new user account.
        email (str): The email address of the new user.
        first_name (str): The first name of the new user.
        last_name (str): The last name of the new user.
        request (HttpRequest): The HTTP request object, used for sending emails.

    Returns:
        User: The newly created user object.

    Raises:
        ValidationError: If a user with the provided username already exists.
    """
    try:
        # user = User(first_name=first_name, last_name=last_name,
        #             username=username, email=email, is_active=False)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True
        )
        user.set_password(password)
        user.save()
        # UserUtils.send_email(request, mail_subject='Activate your account',
        #                      template_path='account_activation_template.html', user=user, receiver=email)
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


def login_user(request, username, password):
    if not username or not password:
        raise ValidationError("Username and password are required.")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError("The provided credentials are invalid.")

    if not user.is_active:
        raise ValidationError(
            "User account is not active. Please activate your account first.")

    flag = authenticate(request, username=username, password=password)

    if not flag:
        raise ValidationError("The provided credentials are invalid.")

    logged_devices = AuthToken.objects.filter(user=user).count()
    if logged_devices >= 5:
        raise ValidationError(
            "Maximum number of devices logged in. Please log out from another device.")

    token = AuthToken.objects.create(user)
    login(request, flag)

    return {'username': user.username, 'token': token[1]}


def update_user_data(user_id, data):
    """
    Updates user data for a given user ID.

    This function attempts to update the user information based on the provided 
    data dictionary. It retrieves the user by ID, updates the fields, and saves 
    the changes. If the user does not exist or if there are validation errors, 
    appropriate exceptions are raised.

    Args:
        user_id (int): The unique identifier of the user to update.
        data (dict): A dictionary containing the fields to update.

    Returns:
        User: The updated user object.

    Raises:
        ValidationError: If no user with the given ID exists or if there are validation errors.
    """
    try:
        user = User.objects.get(id=user_id)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return user
    except User.DoesNotExist:
        raise ValidationError("User not found.")
    except Exception as e:
        raise ValidationError(f"Failed to update user: {str(e)}")


def delete_user(user_id):
    """
    Deletes a user with the given user ID.

    This function attempts to delete a user from the database using the provided 
    user ID. If the user exists, they are deleted. If no user is found with the 
    given ID, a ValidationError is raised.

    Args:
        user_id (int): The unique identifier of the user to delete.

    Returns:
        str: A success message indicating that the user has been deleted.

    Raises:
        ValidationError: If no user with the given ID exists or other deletion error occurs.
    """
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return "User deleted successfully."
    except User.DoesNotExist:
        raise ValidationError("User not found.")
    except Exception as e:
        raise ValidationError(f"Failed to delete user: {str(e)}")


def get_all_users():
    """
    Retrieves all users in the system.

    This function fetches all user objects from the database and returns a list 
    of serialized user data. If an error occurs during retrieval, a ValidationError 
    is raised.

    Returns:
        list: A list of dictionaries containing user data.

    Raises:
        ValidationError: If there is an error retrieving users.
    """
    try:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data
    except Exception as e:
        raise ValidationError(f"Failed to retrieve users: {str(e)}")
