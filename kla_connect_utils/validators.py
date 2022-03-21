from rest_framework.validators import UniqueTogetherValidator
from rest_framework.serializers import ValidationError


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
