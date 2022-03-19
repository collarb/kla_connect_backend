from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer, KlaConnectUserProfile, \
    KlaConnectVerifyProfileSerializer, SimpleKlaConnectLanguage, DetailLanguageSerializer
from kla_connect_profiles.models import ProfileValidation, KlaConnectLanguage
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.db.models import Q


class LanguageViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = SimpleKlaConnectLanguage
    queryset = KlaConnectLanguage.objects.all()
    permission_classes = (AllowAny,)
    lookup_value_regex = '[-\w.]+'
    
    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = DetailLanguageSerializer
        return super(LanguageViewSet,self).retrieve(request,*args,**kwargs)


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = KlaConnectUserProfileSerializer
    queryset = KlaConnectUserProfile.objects.filter(user__deleted=False)
    permission_classes = (IsAuthenticated, DRYPermissions)
    lookup_value_regex = '[-\w.]+'

    def perform_destroy(self, instance):
        user = instance.user
        user.deleted = True
        user.save()

    @action(methods=['post','get'],
            detail=False,
            url_path="verify",
            url_name="verify-profile",
            permission_classes=[AllowAny],
            serializer_class=KlaConnectVerifyProfileSerializer)
    def verify_profile(self, request, format=None):
        """
            verify user profile
        """
        verification_data = {}
        if request.method=='post':
            verification_data = request.data
        else:
            verification_data = request.GET
        serialized_data = self.get_serializer(data=verification_data)
        if serialized_data.is_valid():
            verification_email = serialized_data.data.get('email')
            verification_mobile = serialized_data.data.get('phone')
            verification_code = serialized_data.data.get('verification_code')
            try:
                validation_instance = ProfileValidation.objects.get(
                    (
                        Q(profile__user__email=verification_email) |
                        Q(profile__mobile_number=verification_mobile)
                    ),
                    code=verification_code
                )
                user_profile = validation_instance.profile
                user_profile.verified = True
                user_profile.save()
                if format == 'json':
                    return Response({
                        'verified': True,
                        "message": "Account verified succesfully"
                    }, status=status.HTTP_200_OK)
                else:
                    return redirect('profile_validated')
            except ProfileValidation.DoesNotExist:
                message = "Can not verify profile with email \
                    {} using verification code {}".format(
                    verification_email,
                    verification_code
                )
        else:
            message = serialized_data.errors

        if format == "json":
            return Response({
                'errors': message
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return render(request, 'kla_connect_profiles/verification_failed.html', {
                'message': message
            })


class VerificationSuccessTemplate(TemplateView):
    template_name = "kla_connect_profiles/verified_profile.html"


profile_verified = VerificationSuccessTemplate.as_view()
