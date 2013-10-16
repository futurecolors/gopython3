from rest_framework import serializers
from core.models import Job, Spec


class SpecSetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='get_identifier')
    version = serializers.Field(source='version')
    name = serializers.Field(source='name')

    class Meta:
        model = Spec
        lookup_field = 'code'
        fields = ('id', 'url', 'name', 'version')


class JobSerializer(serializers.HyperlinkedModelSerializer):
    """ Custom job serializer to rename some fields"""
    status = serializers.Field(source='status')

    class Meta:
        model = Job
        fields = ('id', 'url', 'status',
                  'created_at', 'updated_at', 'started_at', 'finished_at', )


class JobDetailSerialzier(JobSerializer):
    packages = SpecSetSerializer(source='specs', many=True)
    status = serializers.Field(source='status')

    class Meta:
        model = Job
        fields = ('id', 'url', 'status', 'packages',
                  'created_at', 'updated_at', 'started_at', 'finished_at', )



class PyPIField(serializers.WritableField):

    def to_native(self, obj):
        latest_obj = obj.get_latest_version()
        return {
            "current": {
                "url": obj.pypi_url,
                "version": obj.version,
                "python3": obj.python_versions,
                "release_date": obj.release_date
            },
            "latest": {
                "url": latest_obj.pypi_url,
                "version": latest_obj.version,
                "python3": latest_obj.python_versions,
                "release_date": latest_obj.release_date
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


class PullRequestField(serializers.WritableField):

    def to_native(self, obj):
        return [{
            "url": obj.pr_url,
            "status": obj.pr_status
        }]


class ForkField(serializers.WritableField):

    def to_native(self, obj):
        if not obj.fork_url:
            return []
        else:
            return [{
                "url": obj.fork_url,
            }]


class CIField(serializers.WritableField):

    def to_native(self, obj):
        return {
            "url": obj.ci_url,
            "status": obj.ci_status
        }


class PackageSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.Field(source='code')
    name = serializers.Field(source='package.name')
    pypi = PyPIField(source='*')
    repo = RepoField(source='package')
    issues = IssueField(source='package')
    forks = ForkField(source='package')
    ci = CIField(source='package')
    pr = PullRequestField(source='package')
    url = serializers.HyperlinkedIdentityField(view_name='spec-detail', lookup_field='code')

    class Meta:
        model = Spec
        fields = ('id', 'name', 'version', 'status',
                  'created_at', 'updated_at', 'pypi', 'repo',
                  'issues', 'forks', 'ci', 'url')
