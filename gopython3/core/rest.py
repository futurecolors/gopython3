from django.db import transaction
from rest_framework import viewsets, routers, serializers, status, mixins
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from core.serializers import JobSerializer, PyPIField, RepoField, IssueField, ForkField, CIField

from .models import Job, Spec
from .tasks import process_job


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


class PackageSerializer(serializers.ModelSerializer):
    id = serializers.Field(source='code')
    name = serializers.Field(source='package.name')
    created_at = serializers.DateTimeField(source='created')
    updated_at = serializers.DateTimeField(source='modified')
    pypi = PyPIField(source='*')
    repo = RepoField(source='package')
    issues = IssueField(source='package')
    forks = ForkField(source='package')
    ci = CIField(source='package')

    class Meta:
        model = Spec
        fields = ('id', 'name', 'version', 'package', 'status',
                  'created_at', 'updated_at', 'pypi', 'repo',
                  'issues', 'forks', 'ci')


class PackageView(RetrieveAPIView):
    model = Spec
    serializer_class = PackageSerializer
    lookup_field = 'code'


router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
