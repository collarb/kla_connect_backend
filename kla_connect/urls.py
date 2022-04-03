"""kla_connect URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from kla_connect_auth.views import UserCreateView, UserView, UserDetailsView, KlaConnectObtainTokenView
from kla_connect_profiles.views import ProfileViewSet, profile_verified, LanguageViewSet, DesignationViewSet, DepartmentViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from kla_connect_location.views import LocationViewSet, LocationDetailViewSet
from kla_connect_incidents.views import IncidentTypeViewSet, IncidentViewSet, ReportTypeViewSet, ReportViewSet,\
    ReportLikeViewSet
from kla_connect_utils.views import NotificationsViewSet
from django.conf import settings
from notifications import urls as notify_urls

schema_view = get_schema_view(
    openapi.Info(
        title="KCCA KLACONNECT API",
        default_version='v1',
        description="KLACONNECT API",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'users/register', UserCreateView)
router.register(r'users', UserView)
router.register(r'profile', ProfileViewSet, basename='Profiles')
router.register(r'desgination', DesignationViewSet, basename='desgination')
router.register(r'department', DepartmentViewSet, basename='department')
router.register(r'location', LocationViewSet, basename='Location')
router.register(r'location', LocationDetailViewSet, basename='Location')
router.register(r'incident/type', IncidentTypeViewSet,
                basename='Incident-types')
router.register(r'incident', IncidentViewSet, basename='Incident')
router.register(r'report/type', ReportTypeViewSet, basename='Report-types')
router.register(r'report/like', ReportLikeViewSet, basename='Report-likes')
router.register(r'report', ReportViewSet, basename='Incidents')
router.register(r'language', LanguageViewSet, basename="Languages")
router.register(r'notifications', NotificationsViewSet,
                basename="Notifications")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/token/', KlaConnectObtainTokenView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/account/me', UserDetailsView.as_view(), name="user-details"),
    path('api/profile/verified/', profile_verified, name="profile_validated"),
    path('api/', include(router.urls)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
