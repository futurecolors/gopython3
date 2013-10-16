from autoslug import AutoSlugField
from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField
from model_utils import Choices
from model_utils.fields import StatusField, AutoCreatedField, AutoLastModifiedField
import requirements


TASK_STATUS = Choices('pending', 'running', 'completed')

from django.conf import settings

if settings.DEBUG:
    import warnings
    warnings.filterwarnings(
            'error', r"DateTimeField received a naive datetime",
            RuntimeWarning, r'django\.db\.models\.fields')


class TimeStampedModel(models.Model):
    created_at = AutoCreatedField('created')
    updated_at = AutoLastModifiedField('modified')

    class Meta:
        abstract = True


class TimeFrameStampedModel(TimeStampedModel):
    STATUS = TASK_STATUS
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def do_start(self):
        self.status = self.STATUS.running
        self.started_at = now()
        self.save(update_fields=['status', 'started_at'])

    def do_finish(self):
        self.status = self.STATUS.completed
        self.finished_at = now()
        self.save(update_fields=['status', 'finished_at'])

    class Meta:
        abstract = True


class JobManager(models.Manager):

    def create_from_requirements(self, requirements_txt_content):
        """ Create job from requirements.txt contents
        """
        job = Job.objects.create(requirements=requirements_txt_content)
        reqs_list = requirements.parse(job.requirements)

        for req in reqs_list:
            line = Line.objects.create(job=job, spec=None, text=req.line)  # spec is calculated later

        return job


class Job(TimeFrameStampedModel):
    """ List of requirements task to check python 3 support of

        Job is defined by its spec set, which is, essentially,
        a list of requirements (ideally, frozen), much like a requirements.txt

        Notes:
            * VCS dependencies are ignored
    """
    requirements = models.TextField()
    status = StatusField()
    specs = models.ManyToManyField('Spec', through='Line', blank=True, null=True)

    objects = JobManager()

    def get_status(self):
        if (self.status == 'completed' and
            self.specs.filter(status__in=['pending', 'running']).count()):
            return 'running'
        return self.status

    def start(self):
        from .tasks import process_requirement
        return [process_requirement.delay(line.pk) for line in self.lines.all()]

    def __str__(self):
        return 'Job %s [%s]' % (self.pk, self.status)


class Line(models.Model):
    """ A line of requirements.txt
        This model serves one purpose: to maintain order of specs in job
        We can not use default intermediate m2m model, because one FKs needs to be nullable
        (so that we can defer spec calculation)
    """
    job = models.ForeignKey(Job, related_name='lines')
    spec = models.ForeignKey('Spec', null=True, related_name='lines')
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text

    def set_distribution(self, distribution):
        """ Set to job line

            Returns tuple (package, package_created, spec, spec_created)
        """
        package, package_created = Package.objects.get_or_create(name=distribution.name)
        spec, spec_created = Spec.objects.get_or_create(package=package, version=distribution.version)
        self.spec = spec
        self.save()
        return package, package_created, spec, spec_created


class Package(TimeStampedModel):
    """ A python package, defined by its name on PyPI

        Notes:
            * All version-specific info is in Spec model
            * Non-PyPI info is pulled for latest repo version
    """
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, slugify=lambda name: name.lower().replace('-', '_'),
                         help_text='Underscore, lowercased')

    # Repo data
    repo_url = models.URLField(blank=True)
    repo_last_commit_date = models.DateTimeField(blank=True, null=True)

    # Issues (one for now)
    ISSUE_STATUS = Choices('unknown', 'open', 'closed')
    issue_url = models.URLField(blank=True)
    issue_status = models.CharField(choices=ISSUE_STATUS, default=ISSUE_STATUS.unknown, max_length=20)

    # PR (one for now)
    pr_url = models.URLField(blank=True)
    pr_status = models.CharField(choices=ISSUE_STATUS, default=ISSUE_STATUS.unknown, max_length=20)

    # Forks (one for now)
    fork_url = models.URLField(blank=True)

    # CI
    CI_STATUS = Choices('unknown', 'passed', 'failed', 'errored')
    ci_url = models.URLField(blank=True)
    ci_status = models.CharField(choices=CI_STATUS, default=CI_STATUS.unknown, max_length=20)

    # Comments
    comment_count = models.IntegerField(default=0)
    comment_most_voted = models.TextField(blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.slug)


class Spec(TimeFrameStampedModel):
    """ A python package with pinned version.
        Contains all metadata, relevant to python 3 current support.
    """
    STATUS = TASK_STATUS

    code = models.CharField(max_length=100, unique=True)
    status = StatusField()
    package = models.ForeignKey('Package')
    version = models.CharField(max_length=20)
    release_date = models.DateTimeField(blank=True, null=True)
    python_versions = JSONField(blank=True, null=True)

    def __str__(self):
        return '%s==%s' % (self.package.name, self.version)

    @property
    def name(self):
        return self.package.name

    def get_identifier(self):
        return '%s/%s' % (self.package.slug, self.version)

    @property
    def pypi_url(self):
        return "https://pypi.python.org/pypi/%s" % self.code

    def get_latest_version(self):
        # TODO: handle blank release dates
        return Spec.objects.filter(package=self.package).latest('release_date')

    def __repr__(self):
        return '<Spec: %s==%s>' % (self.name, self.version)

    def save(self, **kwargs):
        self.code = self.get_identifier()
        super(Spec, self).save(**kwargs)

    class Meta:
        unique_together = (('package', 'version'),)
        index_together = unique_together
