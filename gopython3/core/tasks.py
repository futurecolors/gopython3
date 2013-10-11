from celery.task import task
from distlib.locators import locate


@task
def process_requirement(req, job_id):
    """ Process requirement

        Receives a named tuple of parsed requirement:
        >>> req.name, req.specs, req.extras
        ('Django', [('>=', '1.5'), ('<', '1.6')], [])
    """
    from .models import Package, Spec, JobSpec

    # E.g.: Django (>= 1.0, < 2.0, != 1.3
    distlib_line = req.name
    if req.specs:
        distlib_line += ' (%s)' % (', '.join('%s %s' % cond for cond in req.specs))

    # Returned object has canonical name (flask -> Flask)
    distribution = locate(distlib_line)

    package, _ = Package.objects.get_or_create(name=distribution.name)
    spec, _ = Spec.objects.get_or_create(package=package, version=distribution.version)
    JobSpec.objects.create(job_id=job_id, spec=spec)
