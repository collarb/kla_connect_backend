from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, \
    ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from kla_connect_auth.serializers import KlaConnectUserSerializer, KlaConnectUser, KlaConnectUpdateUserSerializer
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import DEFAULT_FILTER_BACKENDS

class UserCreateView(CreateModelMixin, GenericViewSet):
    serializer_class = KlaConnectUserSerializer
    queryset = KlaConnectUser.objects.all()
    permission_classes = ()


class UserView(ListModelMixin, RetrieveModelMixin,
               UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = KlaConnectUpdateUserSerializer
    queryset = KlaConnectUser.objects.filter(deleted=False)
    filter_backends = DEFAULT_FILTER_BACKENDS

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()


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
