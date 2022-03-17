from kla_connect_utils.serializers import SimpleUserSerializer, KlaConnectUserProfile, \
    serializers, NestedModelSerializer, SimpleKlaConnectLanguage
from kla_connect_profiles.models import KlaConnectLanguageWord


class KlaConnectLanguageWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectLanguageWord
        fields = '__all__'

    def to_representation(self, instance):
        return {
            instance.key: instance.word
        }


class DetailLanguageSerializer(SimpleKlaConnectLanguage):
    words = KlaConnectLanguageWordSerializer(
        many=True, source="language_words")
    
    def to_representation(self, instance):
        data = super(DetailLanguageSerializer,self).to_representation(instance)
        formated_words = {}
        for word in data['words']:
            formated_words = {**formated_words, **word }
        data['words'] = formated_words
        return data

class KlaConnectUserProfileSerializer(NestedModelSerializer):

    user = SimpleUserSerializer

    class Meta:
        model = KlaConnectUserProfile
        fields = '__all__'


class KlaConnectVerifyProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    verification_code = serializers.CharField(required=True)

    def validate(self, attrs):
        print("attrrs",attrs)
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError("Either phone number or email must be provided", "detail")
        return super(KlaConnectVerifyProfileSerializer, self).validate(attrs)
