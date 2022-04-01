from rest_framework.views import exception_handler
from rest_framework.response import Response

ignore_views = ['ReportLikeViewSet']

def custom_exception_handler(exc, context):
    if  type(context['view']).__name__ in ignore_views:
        return Response({},status=200)
    
    return exception_handler(exc, context)