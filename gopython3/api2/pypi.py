# coding: utf-8
from distlib.locators import locate
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import pytz
from .base import HammockAPI


class PyPI(HammockAPI):
    base_url = 'http://pypi.python.org/pypi'

    def get_info(self, name, version=None):
        """ Get package info

            JSON: https://pypi.python.org/pypi/requests/json
        """
        package = self.api(name).json.GET().json()
        return {
            'last_release_date': make_aware(parse_datetime(package['urls'][0]['upload_time']), pytz.utc),
            'py3_versions': self.get_py3_versions(package['info']['classifiers']),
        }

    @classmethod
    def get_distribution(cls, requirement):
        """ Resolve requirement

            Receives a named tuple of parsed requirement:
            >>> req.name, req.specs, req.extras
            ('Django', [('>=', '1.5'), ('<', '1.6')], [])
        """
        distlib_line = requirement.name
        if requirement.specs:
            # E.g.: Django (>= 1.0, < 2.0, != 1.3
            distlib_line += ' (%s)' % (', '.join('%s %s' % cond for cond in requirement.specs))

        # Returned object has canonical name (flask -> Flask)
        return locate(distlib_line)

    @classmethod
    def get_py3_versions(cls, classifiers):
        """ Transform classifiers into list of supported 3.X versions
        """
        versions = [classifier.split(' :: ')[-1] for classifier in classifiers
                    if classifier.startswith('Programming Language :: Python')]
        return [version for version in versions if version.startswith('3')]
