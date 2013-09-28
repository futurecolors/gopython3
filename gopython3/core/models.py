from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from jsonfield import JSONField
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel
from core.util import parse_requirements, normalize_package_name


TASK_STATUS = Choices('pending', 'running', 'completed')


class TimeFrameStampedModel(TimeStampedModel):
    start = models.DateTimeField(null=True, blank=True)
    finish = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class JobManager(models.Manager):

    def create_from_requirements(self, requirements):
        """ Create job from requirements.txt contents
        """
        reqs_list = parse_requirements(requirements)
        job = Job.objects.create()
        for package_name, version in reqs_list:
            package, _ = Package.objects.get_or_create(name=package_name,
                                                       slug=normalize_package_name(package_name))
            spec, _ = Spec.objects.get_or_create(package=package, version=version)
            JobSpec.objects.create(job=job, spec=spec)
        return job


class Job(TimeFrameStampedModel):
    """ A worker process to check python 3 support of a list of requirements

        Job is defined by its spec set, which is, essentially,
        a list of requirements (ideally, frozen), much like a requirements.txt

        Notes:
            * VCS dependencies are ignored
    """
    STATUS = TASK_STATUS
    status = StatusField()
    job_specs = models.ManyToManyField('Spec', through='JobSpec', blank=True, null=True)

    objects = JobManager()


class Package(TimeStampedModel):
    """ A python package, defined by its name on PyPI

        Notes:
            * All version-specific info is in Spec model
            * Non-PyPI info is pulled for latest repo version
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(help_text='Underscore, lowercased')

    # Repo data
    repo_url = models.URLField(blank=True)
    repo_last_commit_date = models.DateTimeField(blank=True, null=True)

    # Issues (one for now)
    ISSUE_STATUS = Choices('unknown', 'passed', 'failed')
    issue_url = models.URLField(blank=True)
    issue_status = models.CharField(choices=ISSUE_STATUS, default=ISSUE_STATUS.unknown, max_length=20)

    # Forks (one for now)
    FORK_STATUS = Choices('open', 'closed', 'merged', 'rejected')
    fork_url = models.URLField(blank=True)
    fork_status = models.CharField(choices=FORK_STATUS, default=FORK_STATUS.open, max_length=20)

    # CI
    ci_url = models.URLField(blank=True)
    ci_status = models.URLField(blank=True)

    # Comments
    comment_count = models.IntegerField(default=0)
    comment_most_voted = models.TextField(blank=True)


@python_2_unicode_compatible
class Spec(TimeStampedModel):
    """ A python package with pinned version.
        Contains all metadata, relevant to python 3 current or future support.
    """
    STATUS = TASK_STATUS

    code = models.CharField(max_length=100, unique=True)
    package = models.ForeignKey('Package')
    version = models.CharField(max_length=20)
    release_date = models.DateTimeField(blank=True, null=True)
    python_versions = JSONField(blank=True, null=True)
    status = StatusField()

    @property
    def name(self):
        return self.package.name

    def get_identifier(self):
        return '%s/%s' % (self.package.slug, self.version)

    @property
    def pypi_url(self):
        return "https://pypi.python.org/pypi/%s" % self.code

    def __str__(self):
        return '<Spec: %s==%s>' % (self.name, self.version)

    def save(self, **kwargs):
        self.code = self.get_identifier()
        super(Spec, self).save(**kwargs)

    class Meta:
        unique_together = (('package', 'version'),)
        index_together = unique_together


class JobSpec(TimeFrameStampedModel):
    """ A spec in a job """
    job = models.ForeignKey(Job)
    spec = models.ForeignKey(Spec, related_name='job_specs')
