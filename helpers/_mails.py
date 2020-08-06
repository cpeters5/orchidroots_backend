from django.core.mail import send_mail
from dbmail import send_db_mail
from accounts.models import User
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext as _


class Mail(object):
    """
    Send class has all mails templates needed in wazer software
    """

    @staticmethod
    def verify_email(user, verification_code):
        try:
            app_name = "Orchid Roots"
            send_db_mail(
                'verify-mail',
                user.email,
                {
                    'app_name': app_name,
                    'fullname': user.fullname,
                    'verification_code': verification_code,
                },
            )
        except Exception as e:
            print(str(e))

    @staticmethod
    def forget_password_email(user, forget_pass_code):
        try:
            app_name = "Orchid Roots"
            send_db_mail(
                'reset-passcode',
                user.email,
                {
                    'app_name': app_name,
                    'fullname': user.fullname,
                    'forget_pass_code': forget_pass_code,
                },
                user=user,
            )
        except Exception as e:
            print(str(e))