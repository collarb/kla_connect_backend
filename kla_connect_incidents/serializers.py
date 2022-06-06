from rest_framework import serializers
from kla_connect_incidents.models import KlaConnectIncidentType, KlaConnectIncident, KlaConnectReportType, \
    KlaConnectReport, ReportLike
from kla_connect_location.serializers import SimplAreaSerializer
from kla_connect_utils.serializers import CreateOnlyCurrentUserDefault, transaction
from kla_connect_utils.mixins import GetCurrentUserAnnotatedSerializerMixin
from kla_connect_utils.serializers import SimpleUserSerializer
from kla_connect_auth.serializers import KlaConnectUserSerializer
from kla_connect_auth.models import CustomNotification
from generic_relations.relations import GenericRelatedField
from kla_connect_utils import constants
from rest_framework.exceptions import ValidationError


class KlaConnectIncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectIncidentType
        fields = "__all__"


class KlaConnectReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectReportType
        fields = '__all__'


class KlaConnectLocationAnnotatedSerializer(serializers.Serializer):

    village = serializers.SerializerMethodField()
    parish = serializers.SerializerMethodField()
    division = serializers.SerializerMethodField()

    def get_village(self, obj, serialized=True):
        village = None
        street = obj.affected_area
        if street:
            village = street.parent
            if serialized:
                village = SimplAreaSerializer(street.parent).data

        return village

    def get_parish(self, obj, serialized=True):
        parish = None
        village = self.get_village(obj, serialized=False)
        if village:
            parish = village.parent
            if serialized:
                parish = SimplAreaSerializer(
                    village.parent).data if village.parent else None

        return parish

    def get_division(self, obj, serialized=True):
        division = None
        parish = self.get_parish(obj, serialized=False)
        if parish:
            if serialized:
                division = SimplAreaSerializer(
                    parish.parent).data if parish.parent else None

        return division


class KlaConnectIncidentSerializer(serializers.ModelSerializer,
                                   GetCurrentUserAnnotatedSerializerMixin,
                                   KlaConnectLocationAnnotatedSerializer):

    type_display = KlaConnectIncidentTypeSerializer(
        source='type', read_only=True)
    priority_display = serializers.CharField(read_only=True)
    status_display = serializers.CharField(read_only=True)
    area = SimplAreaSerializer(source="affected_area", read_only=True)
    user = KlaConnectUserSerializer(required=False, read_only=True)

    def create(self, validated_data):
        user = self.get_current_user()
        validated_data['user'] = user
        if not user.is_citizen:
            validated_data['status'] = constants.INCIDENT_STATUS_COMPLETE
        return super(KlaConnectIncidentSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        no_permissions = False
        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user

        # check if user if status change
        status_change_to = validated_data.get('status')
        if status_change_to:
            if status_change_to in [constants.INCIDENT_STATUS_COMPLETE] and not request.user.is_manager:
                no_permissions = True

            if status_change_to in [constants.INCIDENT_STATUS_FOR_REVIEW] and not request.user.is_data_entrant:
                no_permissions = True

        if no_permissions:
            raise ValidationError(
                "You don't have permissions to perform this action"
            )
        validated_data['previous_status'] = instance.status
        validated_data['previous_feedback'] = instance.feedback
        return super(KlaConnectIncidentSerializer, self).update(instance, validated_data)

    class Meta:
        model = KlaConnectIncident
        fields = '__all__'
        extra_kwargs = {
            'type': {'write_only': True, 'required': True},
            'status': {'write_only': True, 'required': False},
            'affected_area': {'write_only': True,
                              'required': True}
        }
        read_only_fields = ('ref',)


class KlaConnectReportSerializer(serializers.ModelSerializer,
                                 GetCurrentUserAnnotatedSerializerMixin,
                                 KlaConnectLocationAnnotatedSerializer):

    type_display = KlaConnectIncidentTypeSerializer(
        source='type', read_only=True)
    area = SimplAreaSerializer(source="affected_area", read_only=True)
    user = KlaConnectUserSerializer(required=False, read_only=True)
    views_count = serializers.SerializerMethodField()
    thumbs_up = serializers.SerializerMethodField()
    thumbs_down = serializers.SerializerMethodField()
    status_display = serializers.CharField(read_only=True)

    def create(self, validated_data):
        user = self.get_current_user()
        validated_data['user'] = user
        return super(KlaConnectReportSerializer, self).create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        request = self.context.get("request")
        no_permissions = False

        if request and hasattr(request, "user"):
            user = request.user
            validated_data["author"] = user
        # check if user if status change
        status_change_to = validated_data.get('status')
        if status_change_to:
            if status_change_to in [constants.INCIDENT_REPORT_REJECTED, constants.INCIDENT_STATUS_COMPLETE] and not (request.user.is_manager or request.user.is_ddt):
                no_permissions = True

            if status_change_to in [constants.INCIDENT_STATUS_FOR_REVIEW] and request.user.is_citizen:
                no_permissions = True

        publishing = validated_data.get('published')
        if publishing:
            if not (request.user.is_manager or request.user.is_ddt):
                no_permissions = True

        if no_permissions:
            raise ValidationError(
                "You don't have permissions to perform this action"
            )

        validated_data['previous_status'] = instance.status
        validated_data['previous_feedback'] = instance.feedback
        validated_data['publishing'] = publishing
        return super(KlaConnectReportSerializer, self).update(instance, validated_data)

    class Meta:
        model = KlaConnectReport
        fields = '__all__'
        extra_kwargs = {
            'type': {'write_only': True, 'required': True},
            'status': {'write_only': True, 'required': False},
            'affected_area': {'write_only': True,
                              'required': True}
        }
        read_only_fields = ('ref',)

    def get_views_count(self, obj):
        return obj.views.count()

    def get_thumbs_up(self, obj):
        return obj.likes.filter(thumbs_up=True).count()

    def get_thumbs_down(self, obj):
        return obj.likes.filter(thumbs_up=False).count()


class CustomNotificationSerializer(serializers.ModelSerializer):

    recipient = SimpleUserSerializer(many=False, read_only=True)
    action = serializers.CharField(source='verb')
    activity_type = serializers.SerializerMethodField()
    activity = GenericRelatedField({
        KlaConnectIncident: KlaConnectIncidentSerializer(),
        KlaConnectReport: KlaConnectReportSerializer()
    }, source="action_object")

    class Meta:
        model = CustomNotification
        exclude = (
            "verb",
            "action_object_content_type",
            "action_object_object_id",
            'actor_object_id',
            'actor_content_type',
            'target_object_id',
            'target_content_type'
        )

    def get_activity_type(self, obj):
        return get_instance_type(obj.action_object)


def get_instance_type(instance):
    if instance:
        instance_class = type(instance)
        return instance_class.__name__
    return None


class ReportLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportLike
        fields = "__all__"
