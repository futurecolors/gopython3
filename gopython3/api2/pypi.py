# coding: utf-8
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
import pytz
import requests
from .base import HammockAPI


class PyPI(HammockAPI):
    base_url = 'http://pypi.python.org/pypi'

    def get_info(self, name, version=None):
        """ Get package info

            JSON: https://pypi.python.org/pypi/requests/json
        """
        name = self.get_correct_name(name)
        package = self.api(name).json.GET().json()
        return {
            'last_release_date': make_aware(parse_datetime(package['urls'][0]['upload_time']), pytz.utc),
            'py3_versions': self.get_py3_versions(package['info']['classifiers']),
            'name': name
        }

    def get_correct_name(self, name):
        """ Naturally PyPI redirects us into correct URL
            E.g. https://pypi.python.org/simple/DJANGO/ -> https://pypi.python.org/simple/Django/
            That's generally faster than XMLRPC: https://wiki.python.org/moin/PyPIXmlRpc method
        """
        response = requests.get('http://pypi.python.org/simple/%s/' % name)
        return response.url.split('/')[-2]

    @classmethod
    def get_py3_versions(cls, classifiers):
        """ Transform classifiers into list of supported 3.X versions
        """
        versions = [classifier.split(' :: ')[-1] for classifier in classifiers
                    if classifier.startswith('Programming Language :: Python')]
        return [version for version in versions if version.startswith('3')]
