from kla_connect_utils.models import models, TimeStampModel
from dry_rest_permissions.generics import allow_staff_or_superuser

class Area(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    parent = models.ForeignKey('kla_connect_location.Area', related_name="child_areas", 
                               on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        display_name = self.name
        if self.parent:
            display_name = '{} / {}'.format(display_name,self.parent)
        return display_name
    
    def __repr__(self):
        return self.__str__()
    
    @staticmethod
    def has_object_write_permission(request):
        return request.user.is_superuser
    
    @staticmethod
    def has_write_permission(request):
        return request.user.is_superuser
    
    @staticmethod
    def has_read_permission(request):
        return True
    
    @staticmethod
    def has_object_read_permission(request):
        return True