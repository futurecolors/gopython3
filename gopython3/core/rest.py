from django.db import transaction
from rest_framework import viewsets, routers, serializers, status, mixins
from rest_framework.response import Response

from .models import Job, JobSpec
from .tasks import process_job


class SpecSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='spec.identifier')
    version = serializers.Field(source='spec.version')
    name = serializers.Field(source='spec.name')
    status = serializers.Field(source='spec.status')
    created_at = serializers.DateTimeField(source='created')
    updated_at = serializers.DateTimeField(source='modified')
    started_at = serializers.DateTimeField(source='start')
    finished_at = serializers.DateTimeField(source='finish')

    class Meta:
        model = JobSpec
        fields = ('id', 'name', 'version', 'status',
                  'created_at', 'updated_at', 'started_at', 'finished_at',)


class JobSerializer(serializers.HyperlinkedModelSerializer):
    """ Custom job serializer to rename some fields"""
    created_at = serializers.DateTimeField(source='created')
    updated_at = serializers.DateTimeField(source='modified')
    started_at = serializers.DateTimeField(source='start')
    finished_at = serializers.DateTimeField(source='finish')
    packages = SpecSetSerializer(source='jobspec_set', many=True)

    class Meta:
        model = Job
        fields = ('id', 'url', 'packages', 'status',
                  'created_at', 'updated_at', 'started_at', 'finished_at', )


class JobViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                job = Job.objects.create_from_requirements(request.DATA['requirements'])
                serializer = self.get_serializer(job)
                headers = self.get_success_headers(serializer.data)
        except Exception as e:
            return Response({'requirements': 'Bad requirements. %s' % e},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            process_job.delay(job.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
