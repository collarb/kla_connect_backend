from kla_connect_profiles.models import KlaConnectUserProfile, ProfileValidation
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from kla_connect_utils.email_utils import send_email


@receiver(post_save, sender=KlaConnectUserProfile)
def handle_profile_verification(sender, instance, created, **kwargs):
    if created:
        # send otp
        ProfileValidation.objects.create(profile=instance)
    else:
        if instance.verified and instance.profilevalidation_set.exists():
            instance.profilevalidation_set.delete()


@receiver(post_save, sender=ProfileValidation)
def send_otp_email(sender, instance, created, **kwargs):
    if created:
        send_to_email = instance.profile.user.email
        msg_html = render_to_string(
            'kla_connect_profiles/email/verification_email_template', {
                'email': send_to_email,
                'code': instance.code
            })
        send_email(message=msg_html,
                   subject="Email verification/Profile Activation: KCCA KLA_CONNECT",
                   send_to_email)
