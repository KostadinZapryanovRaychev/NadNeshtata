import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .models import User


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """Token generator"""

    def _make_hash_value(self, user: User, timestamp):
        return (
            six.text_type(User.pk) + six.text_type(timestamp) +
            six.text_type(User.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
