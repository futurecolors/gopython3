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
                  https://pypi.python.org/pypi/requests/2.0.0/json
        """
        path = '%s/%s' % (name, version) if version else name
        package = self.api(path).json.GET().json()
        # FIXME: no upload time?
        # FIXME: no classifiers?
        return {
            'last_release_date': make_aware(parse_datetime(package['urls'][0]['upload_time']), pytz.utc),
            'py3_versions': self.get_py3_versions(package['info']['classifiers']),
            'url': package['info'].get('home_page', ''),
            'name': package['info']['name']
        }

    @classmethod
    def get_distribution(cls, requirement):
        """ Resolve requirement

            Receives a named tuple of parsed requirement:
            Requirement(name='Django', specs=[('>=', '1.5'), ('<', '1.6')], extras=[])
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
