from kla_connect_utils.serializers import SimpleUserSerializer, KlaConnectUserProfile, \
    serializers, NestedModelSerializer, SimpleKlaConnectLanguage
from kla_connect_profiles.models import KlaConnectLanguageWord, Department, Designation
from kla_connect_utils.validators import CustomUniqueValidator
from kla_connect_utils.constants import NATIONALITY_UG


class KlaConnectLanguageWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectLanguageWord
        fields = '__all__'

    def to_representation(self, instance):
        return {
            instance.key: instance.word
        }


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DetailLanguageSerializer(SimpleKlaConnectLanguage):
    words = KlaConnectLanguageWordSerializer(
        many=True, source="language_words")

    def to_representation(self, instance):
        data = super(DetailLanguageSerializer,
                     self).to_representation(instance)
        formated_words = {}
        for word in data['words']:
            formated_words = {**formated_words, **word}
        data['words'] = formated_words
        return data


class KlaConnectUserProfileSerializer(NestedModelSerializer):

    user = SimpleUserSerializer

    class Meta:
        model = KlaConnectUserProfile
        fields = '__all__'
        validators = [
            CustomUniqueValidator(
                queryset=KlaConnectUserProfile.objects.all(),
                fields=['id_type', 'id_number']
            ),
            CustomUniqueValidator(
                queryset=KlaConnectUserProfile.objects.all(),
                fields=['nin', ]
            )
        ]

    def validate(self, attrs):
        attrs = super(KlaConnectUserProfileSerializer, self).validate(attrs)
        if not attrs.get("designation"):
            nationality_value = attrs.get("nationality")
            if nationality_value == NATIONALITY_UG:
                if not attrs.get("nin"):
                    raise serializers.ValidationError(
                        {"nin": "nin is required for Ugandans"}, "required")
            else:
                if not attrs.get("id_type"):
                    raise serializers.ValidationError(
                        {"id_type": "id_type is required for non Ugandans"}, "required")

                if not attrs.get("id_number"):
                    raise serializers.ValidationError(
                        {"id_number": "id_number is required for non Ugandans"}, "required")

        return attrs


class KlaConnectVerifyProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    verification_code = serializers.CharField(required=True)

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError(
                "Either phone number or email must be provided", "detail")
        return super(KlaConnectVerifyProfileSerializer, self).validate(attrs)
