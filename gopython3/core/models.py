from django.db import models
from model_utils import Choices
from model_utils.fields import StatusField
from model_utils.models import TimeStampedModel


TASK_STATUS = Choices('pending', 'running', 'completed')


class TimeFrameStampedModel(TimeStampedModel):
    start = models.DateTimeField(null=True, blank=True)
    finish = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Job(TimeFrameStampedModel):
    """ A worker process to check python 3 support of a list of requirements

        Job is defined by its spec set, which is, essentially,
        a list of requirements (ideally, frozen), much like a requirements.txt

        Notes:
            * VCS dependencies are ignored
    """
    STATUS = TASK_STATUS

    specs = models.ManyToManyField('Spec')
    status = StatusField()


class Package(TimeStampedModel):
    """ A python package, defined by its name on PyPI

        Notes:
            * All version-specific info is in Spec model
            * Non-pypi info is pulled for latest repo version
    """
    name = models.CharField(max_length=100)

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


class Spec(TimeFrameStampedModel):
    """ A python package with pinned version.
        Contains all metadata, relevant to python 3 current or future support.
    """
    STATUS = TASK_STATUS
    GOPY3 = Choices(('A', 'Already supports'),
                    ('B', 'Future version or trunk'),
                    ('C', 'Fork or PR'))

    package = models.ForeignKey('Package')
    version = models.CharField(max_length=20)
    gopy3 = models.CharField(choices=GOPY3, default=GOPY3.A, max_length=20)
    status = StatusField()

    class Meta:
        unique_together = (('package', 'version'),)
        index_together = unique_together
