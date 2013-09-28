from distlib.locators import locate
from django.utils.dateparse import parse_datetime
from api import abstract_wrappers


class PyPIWrapper(abstract_wrappers.AbstractJsonApiWrapper):
    base_url = 'http://pypi.python.org/pypi'

    def package_info(self, name, version=None):
        self.hammock = self.hammock(name)
        if version:
            self.hammock = self.hammock(version)
        self.hammock = self.hammock.json
        return 'GET', {}

    def get_short_info(self, name, version=None):
        name = self.get_correct_name(name)
        data = self.ask_about_package_info(name=name, version=version)
        return {
            'last_release_date': parse_datetime(data['urls'][0]['upload_time']),
            'python3_supported_versions': list(self.get_py3_supported_versions(data)),
            'url': data['info']['package_url'],
            'name': name,
            'version': data['info']['version']
        }

    def get_py3_supported_versions(self, data):
        language_classifiers = data['info']['classifiers']
        python_info = filter(lambda c: c.startswith('Programming Language') and 'Python' in c, language_classifiers)
        py3_versions = filter(lambda v: v[0] == '3', [v.split('::')[-1].strip() for v in python_info])
        return py3_versions

    def get_correct_name(self, name):
        return locate(name).name
