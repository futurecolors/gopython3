from rest_framework import serializers
from core.models import JobSpec, Job, Spec


class SpecSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='spec.get_identifier')
    version = serializers.Field(source='spec.version')
    name = serializers.Field(source='spec.name')
    status = serializers.Field(source='status')
    created_at = serializers.DateTimeField(source='created')
    updated_at = serializers.DateTimeField(source='modified')
    started_at = serializers.DateTimeField(source='start')
    finished_at = serializers.DateTimeField(source='finish')

    class Meta:
        model = JobSpec
        lookup_field = 'code'
        fields = ('id', 'url', 'name', 'version', 'status',
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
