from rest_framework import viewsets, routers, mixins, serializers
from core.models import Job


class JobSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.DateTimeField(source='created')
    updated_at = serializers.DateTimeField(source='modified')
    started_at = serializers.DateTimeField(source='start')
    finished_at = serializers.DateTimeField(source='finish')

    class Meta:
        model = Job
        fields = ('id', 'url', 'status', 'created_at',
                  'updated_at', 'started_at', 'finished_at')


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer


router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
