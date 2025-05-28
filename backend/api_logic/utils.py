from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage


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
