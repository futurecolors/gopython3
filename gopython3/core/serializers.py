from rest_framework import serializers
from core.models import JobSpec, Job


class SpecSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='spec.get_identifier')
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


class PyPIField(serializers.WritableField):

    def to_native(self, obj):
        return {
            "current": {
                "url": obj.pypi_url,
                "version": obj.version,
                "python3": obj.python_versions,
                "release_date": obj.release_date
            },
            "latest": {
                "url": obj.pypi_url,
                "version": obj.version,
                "python3": obj.python_versions,
                "release_date": obj.release_date
            }
        }


class RepoField(serializers.WritableField):

    def to_native(self, obj):
        return {
            "url": obj.repo_url,
            "last_commit_date": obj.repo_last_commit_date
        }


class IssueField(serializers.WritableField):

    def to_native(self, obj):
        return [{
            "url": obj.issue_url,
            "status": obj.issue_status
        }]


class ForkField(serializers.WritableField):

    def to_native(self, obj):
        return [{
            "url": obj.fork_url,
            "status": obj.fork_status
        }]


class CIField(serializers.WritableField):

    def to_native(self, obj):
        return [{
            "url": obj.ci_url,
            "status": obj.ci_status
        }]
