from kla_connect_utils.serializers import NestedModelSerializer, serializers
from kla_connect_location.models import Area

class SimplAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        exclude = ('parent',)

class AreaSerializer(NestedModelSerializer, SimplAreaSerializer):
    areas = SimplAreaSerializer(many=True,source="child_areas",required=False)
        