from django.db import transaction
from rest_framework import viewsets, routers, status, mixins
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_extensions.mixins import DetailSerializerMixin
from core.serializers import JobSerializer, PackageSerializer, JobDetailSerialzier

from .models import Job, Spec


class JobViewSet(DetailSerializerMixin, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    model = Job
    serializer_class = JobSerializer
    serializer_detail_class = JobDetailSerialzier

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
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


class PackageView(RetrieveAPIView):
    model = Spec
    serializer_class = PackageSerializer
    lookup_field = 'code'


router = routers.DefaultRouter()
router.register(r'jobs', JobViewSet)
