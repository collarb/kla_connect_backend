from django.conf import settings
from django.core.mail import EmailMessage


def send_email(mail_from=None, message=None, subject=None, mail_to:[str, list]=None):

    mail_from = getattr(
        settings, 'DEFAULT_FROM_EMAIL') if mail_from is None else mail_from
    mail_to = [mail_to] if not isinstance(mail_to, list) else mail_to
    msg = EmailMessage(subject, message, mail_from,mail_to)
    msg.content_subtype = 'html'
    msg.send()
