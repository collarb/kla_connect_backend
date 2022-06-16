from collections import OrderedDict
from rest_framework import serializers
from kla_connect_profiles.models import KlaConnectUserProfile, get_user_model, KlaConnectLanguage, Address, VistedAddress
from django.db import transaction
from kla_connect_utils.constants import ADDRESSES_CHOICES, VISTED_ADDRESS, HOME_ADDRESS, WORK_ADDRESS
from kla_connect_utils.mixins import GetCurrentUserAnnotatedSerializerMixin


class CreateOnlyCurrentUserDefault(serializers.CurrentUserDefault):

    def set_context(self, serializer_field):
        self.is_update = serializer_field.parent and serializer_field.parent.instance is not None
        super(CreateOnlyCurrentUserDefault, self).set_context(serializer_field)

    def __call__(self):
        if hasattr(self, 'is_update') and self.is_update:
            # TODO: Make sure this check is sufficient for all update scenarios
            raise SkipField()
        user = super(CreateOnlyCurrentUserDefault, self).__call__()
        if user and user.is_authenticated:
            return user
        return None


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class VisitedAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    
    class Meta:
        model = VistedAddress
        fields = ('address',)
    
    def to_representation(self, instance):
        data = super(VisitedAddressSerializer, self).to_representation(instance)
        return data['address']
    
class CreateAddressSerializer(AddressSerializer,
                              GetCurrentUserAnnotatedSerializerMixin):
    type = serializers.ChoiceField(
        ADDRESSES_CHOICES, default=VISTED_ADDRESS, write_only=True)

    def create(self, attrs):
        address_type = attrs.pop('type')
        new_address = super(CreateAddressSerializer, self).create(attrs)
        current_user = self.get_current_user()
        try:
            if address_type == VISTED_ADDRESS:
                VistedAddress.objects.create(
                    user=current_user, address=new_address)
            elif address_type == HOME_ADDRESS:
                user_profile = current_user.profile
                user_profile.home_address = new_address
                user_profile.save()
            elif address_type == WORK_ADDRESS:
                user_profile = current_user.profile
                user_profile.work_address = new_address
                user_profile.save()
        except Exception as e:
            raise serializers.ValidationError({"error":str(e)})
        return new_address


class NestedModelSerializer(serializers.ModelSerializer):

    @transaction.atomic
    def create(self, validated_data):
        return self.nested_save_override(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        return self.nested_save_override(validated_data, instance=instance)

    @transaction.atomic
    def nested_save_override(self, validated_data, instance=None):
        nested_method_models = []
        nested_data = []

        field_source_map = dict()
        for field_key in self.get_fields():
            field_value = self.get_fields().get(field_key, None)
            if field_value:
                source = getattr(field_value, 'source', None)
                if source:
                    field_source_map[source] = field_key

        for attribute_key in self.validated_data.keys():
            clean_attribute_key = field_source_map.get(
                attribute_key, attribute_key)
            save_method = getattr(
                self, 'save_nested_{}'.format(clean_attribute_key), None)
            attribute_value = self.validated_data.get(attribute_key, None)
            if save_method:
                # Filter nested save model data
                if attribute_value:
                    nested_method_models.append((save_method, attribute_value))

                # remove attribute from validated data if it exists
                validated_data.pop(attribute_key)
            elif type(attribute_value) in [dict, list]:
                # Filter nested data
                serializer_field = self.get_fields().get(clean_attribute_key, None)
                if serializer_field:
                    serializer_field_child = getattr(
                        serializer_field, 'child', None)

                    if serializer_field_child:
                        serializer_class = serializer_field_child.__class__
                    else:
                        serializer_class = serializer_field.__class__

                    if serializer_class:
                        fk_keys = []
                        if serializer_class.Meta and serializer_class.Meta.model and self.Meta and self.Meta.model:
                            for model_field in serializer_class.Meta.model._meta.get_fields():
                                if model_field.related_model == self.Meta.model:
                                    fk_keys.append(model_field.name)
                        if isinstance(attribute_value, list):
                            for single_attribute_value in attribute_value:
                                nested_data.append(
                                    (clean_attribute_key, single_attribute_value, serializer_class, fk_keys))
                        else:
                            nested_data.append(
                                (clean_attribute_key, attribute_value, serializer_class, fk_keys))

                # remove attribute from validated data to prevent writable
                # nested non readonly fields error
                validated_data.pop(attribute_key)

            if type(attribute_value) in [dict, OrderedDict]:
                attribute_value_object_id = attribute_value.get('id', None)
                if attribute_value_object_id:
                    serializer_field = self.get_fields().get(clean_attribute_key, None)
                    serializer_class = serializer_field.__class__
                    validated_data[clean_attribute_key] = serializer_class.Meta.model.objects.get(
                        pk=attribute_value_object_id)

        is_created = not bool(instance)
        if instance:
            instance = super(NestedModelSerializer, self).update(
                instance, validated_data)
        else:
            instance = super(NestedModelSerializer,
                             self).create(validated_data)

        try:
            # Saving nested values is best effort
            for attribute_details in nested_method_models:
                save_method = attribute_details[0]
                attribute_value = attribute_details[1]
                if save_method and attribute_value:
                    save_method(attribute_value, instance, created=is_created)

            for (k, v, s, r) in nested_data:
                v = dict(v)
                if r:
                    for related_key in r:
                        v[related_key] = instance
                if s.Meta.model:
                    if 'id' in v:
                        s.Meta.model.objects.update_or_create(
                            id=v['id'], defaults=v)
                    else:
                        s.Meta.model.objects.create(**v)
                else:
                    serializer = s(data=v, **dict(context=self.context))
                    serializer.save()
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return instance


class SimpleProfileSerializer(serializers.ModelSerializer):
    home_address = AddressSerializer(read_only=True)
    work_address = AddressSerializer(read_only=True)

    class Meta:
        model = KlaConnectUserProfile
        exclude = ('user',)
        read_only_fields = ('id', 'verified')


class SimpleUserSerializer(serializers.ModelSerializer):

    is_citizen = serializers.BooleanField(read_only=True)
    is_data_entrant = serializers.BooleanField(read_only=True)
    is_manager = serializers.BooleanField(read_only=True)
    is_ddt = serializers.BooleanField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    display_role = serializers.CharField(read_only=True)

    class Meta:
        model = get_user_model()
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
            'role': {'write_only': True},
        }
        exclude = ('groups', 'user_permissions', 'deleted', 'is_superuser')
        read_only_fields = ('id', 'last_login', 'date_joined', 'is_staff')


class ProfileSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer

    class Meta:
        model = KlaConnectUserProfile
        read_only_fields = ('id', 'verified')


class SimpleKlaConnectLanguage(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectLanguage
        fields = '__all__'
