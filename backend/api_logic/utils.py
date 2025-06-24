from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class HandleResponseUtils(object):
    """This class holds methods related to views.py:
    1. The methods here are related to response handling
    """
    @staticmethod
    def handle_response(status_code, message) -> JsonResponse:
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        # If the obj is type set return list(obj)
        if isinstance(message, set):
            return JsonResponse(data=list(message), status=status_code, safe=False)
        else:
            return JsonResponse(data=message, status=status_code, safe=False)

    @staticmethod
    def handle_response_data(status_code, message):
        """
        Returns proper response data
        :param status_code: http status code
        :type status_code: http status code
        :param message: function that contains response
        :rType: JsonResponse
        :returns: JsonResponse
        """
        if isinstance(message, set):
            return JsonResponse(data=list(message).data, status=status_code, safe=False)
        else:
            return JsonResponse(data=message.data, status=status_code, safe=False)


class UserUtils(object):
    """This class holds methods related to user management:
    1. The methods here are related to user management
    2. The methods here are related to user authentication
    3. The methods here are related to user email handling
    """

    def validate_user_data(*, username: str, email: str,
                           password: str, confirm_password: str) -> bool:
        """
        Validates registration input.

        Rules
        -----
        • Username: ≥ 3 chars, only letters, digits, underscore (_), dot (.) or hyphen (-),
        and must not already exist.
        • Email: valid format and not already registered.
        • Passwords: must match.

        Raises
        ------
        rest_framework.exceptions.ValidationError
            When one or more rules fail.  The exception's `.detail` is a dict
            mapping field names to error messages (DRF will turn it into JSON).

        Returns
        -------
        bool
            True if everything is valid (never returns False—an invalid state raises).
        """
        errors = {}

        # -------- username -------------------------------------------------
        if len(username) < 3:
            errors["username"] = "Username must be at least 3 characters long."
        elif not re.fullmatch(r"^[\w.-]+$", username):
            errors["username"] = (
                "Username can only contain letters, numbers, "
                "underscores (_), dots (.) and hyphens (-)."
            )
        elif User.objects.filter(username=username).exists():
            errors["username"] = f"Username '{username}' is already taken."

        # -------- email ----------------------------------------------------
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Invalid email format."
        else:
            if User.objects.filter(email=email).exists():
                errors["email"] = f"Email '{email}' is already registered."

        # -------- passwords ------------------------------------------------
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match."

        # -------- final ----------------------------------------------------
        if errors:
            raise ValidationError(errors)

        return True

    def send_email(request, mail_subject: str, template_path: str, user: object, receiver: str) -> None:
        """
        Sends an email containing a verification link necessary for account activation.
        :param mail_subject: what is the email about
        :type mail_object: string
        :param template_path: which template to use from templates folder
        :type template_path: string
        :param user: user object
        :type user: object
        :param receiver: the email adress which will receive the message
        :type receiver: string
        :rType: None
        :returns: None, just logs the state of the message.
        """
        mail_subject = mail_subject
        message = render_to_string(template_path,
                                   {
                                       'user': user,
                                       'domain': get_current_site(request).domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': account_activation_token.make_token(user),
                                       'protocol': 'https' if request.is_secure() else 'http',
                                       'new_email': receiver
                                   })

        email = EmailMessage(subject=mail_subject, body=message, to=[receiver])
        send_email = email.send()
        if send_email:
            return True
        else:
            print("Email sending failed.")
            print(f"Email subject: {mail_subject}")
            return False


class AuthorUtils(object):
    """This class holds methods related to author management:
    1. The methods here are related to author management
    """

    @staticmethod
    def validate_author_data(*, bio: str, profile_picture: str) -> bool:
        """
        Validates author data.

        Rules
        -----
        • Bio: can be empty or up to 500 characters.
        • Profile picture: must be a valid URL.

        Raises
        ------
        rest_framework.exceptions.ValidationError
            When one or more rules fail. The exception's `.detail` is a dict
            mapping field names to error messages (DRF will turn it into JSON).

        Returns
        -------
        bool
            True if everything is valid (never returns False—an invalid state raises).
        """
        errors = {}

        if len(bio) > 500:
            errors["bio"] = "Bio cannot exceed 500 characters."

        if not re.match(r'^https?://', profile_picture):
            errors["profile_picture"] = "Profile picture must be a valid URL."

        if errors:
            raise ValidationError(errors)

        return True


class ContentUtils(object):
    """This class holds methods related to content management:
    1. The methods here are related to content management
    """

    @staticmethod
    def validate_content_data(*, title: str, body: str, author: str) -> bool:
        """
        Validates content data.

        Rules
        -----
        • Title: must be at least 3 characters long.
        • Body: must not be empty.

        Raises
        ------
        rest_framework.exceptions.ValidationError
            When one or more rules fail. The exception's `.detail` is a dict
            mapping field names to error messages (DRF will turn it into JSON).
        Returns
        -------
        bool
            True if everything is valid (never returns False—an invalid state raises).
        """
        errors = {}

        if len(title) < 3:
            errors["title"] = "Title must be at least 3 characters long."

        if not body.strip():
            errors["body"] = "Body cannot be empty."

        if not author:
            errors["author"] = "Author must be specified."

        if errors:
            raise ValidationError(errors)

        return True
