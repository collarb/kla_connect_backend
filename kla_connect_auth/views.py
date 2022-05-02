from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, \
    ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from kla_connect_auth.serializers import KlaConnectUserSerializer, KlaConnectUser, KlaConnectUpdateUserSerializer, \
    KlaConnectUserObtainPairSerializer, KlaConnectResetPasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from kla_connect_utils.filterbackends import DEFAULT_FILTER_BACKENDS
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from kla_connect_profiles.models import ProfileValidation
from django.db.models import Q
from rest_framework.decorators import action


class KlaConnectObtainTokenView(TokenObtainPairView):
    serializer_class = KlaConnectUserObtainPairSerializer


class UserCreateView(CreateModelMixin, GenericViewSet):
    serializer_class = KlaConnectUserSerializer
    queryset = KlaConnectUser.objects.all()
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """
            Response
            {
                "message":string
            }
        """
        user_filter_kwargs = Q()
        if request.data.get('email'):
            user_filter_kwargs |= Q(email=request.data['email'])

        if request.data.get('username'):
            user_filter_kwargs |= Q(username=request.data.get('username'))

        if request.data.get('profile'):
            mobile_number = request.data['profile'].get('mobile_number')
            if mobile_number:
                user_filter_kwargs |= Q(
                    profile__mobile_number=mobile_number)

        if bool(user_filter_kwargs):
            instance = self.get_queryset().filter(
                user_filter_kwargs, profile__verified=False).first()
            if instance:
                instance.delete()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(response,
                        status=status.HTTP_201_CREATED)


class UserView(ListModelMixin, RetrieveModelMixin,
               UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = KlaConnectUpdateUserSerializer
    queryset = KlaConnectUser.objects.filter(deleted=False)
    filter_backends = DEFAULT_FILTER_BACKENDS
    filterset_fields = ["role", "gender", "is_active"]
    search_fields = ["username", "last_name", "first_name", "email",
                     "profile__mobile_number", "profile__nin"]

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
    
    @action(methods=['post'],
            detail=False,
            url_path="reset-password",
            url_name="password-reset",
            serializer_class=KlaConnectResetPasswordSerializer,
            permission_classes=[AllowAny])
    def reset_password(self, request, format=None):
        """
        _summary_

        Args:
            request (_type_): _description_
            format (_type_, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        reset_serializer = self.get_serializer(data=request.data)
        reset_serializer.is_valid(raise_exception=True)
        return Response({
            "message": reset_serializer.message
        }, status=status.HTTP_200_OK)
        

class UserDetailsView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        user = request.user
        if user is not None and user.is_authenticated:
            return user
        else:
            return None

    def get(self, request):
        user = self.get_object(request)
        if user is None:
            return Response(
                {'status': 'Unauthorized', 'message': 'You are not logged in'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = KlaConnectUserSerializer(user)
        return Response(serializer.data)
