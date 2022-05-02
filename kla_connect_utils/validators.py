from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import ValidationError
from kla_connect_utils.constants import PASSWORD_RESET_REQUEST_ACTION, PASSWORD_RESET_ACTION


class CustomUniqueValidator(UniqueTogetherValidator):

    def check_if_run(self, attrs):
        run_validator = False
        for field in self.fields:
            if field is not None and attrs.get(field):
                run_validator = run_validator or True

        return run_validator

    def __call__(self, attrs, serializer):
        if self.check_if_run(attrs):
            super(CustomUniqueValidator, self).__call__(attrs, serializer)

class PasswordResetValidators:
    
    def validate_email(self, attrs):
        if attrs.get('action') == PASSWORD_RESET_REQUEST_ACTION:
            if not attrs.get("email"):
                raise ValidationError({"email":"Email or phone number should be provided"},code="required")

    def validate_reset_code(self, attrs):
        if attrs.get('action') == PASSWORD_RESET_ACTION:
            if not attrs.get("reset_code"):
                raise ValidationError({"reset_code":"Reset Code should be provided"})

    def validate_new_password(self, attrs):
        if attrs.get('action') == PASSWORD_RESET_ACTION:
            if not attrs.get("new_password"):
                raise ValidationError({"new_password":"New Password cannot be blank"})
    
    def __call__(self, attrs):
        self.validate_email(attrs)
        self.validate_reset_code(attrs)
        self.validate_new_password(attrs)