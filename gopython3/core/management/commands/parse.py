# coding: utf-8
import logging
from django.core.management.base import LabelCommand
from core.models import Job


class Command(LabelCommand):

    def handle(self, *args, **options):
        logger = logging.getLogger('core')
        logger.setLevel(logging.DEBUG)
        Job.objects.create_from_requirements('\n'.join(args))
