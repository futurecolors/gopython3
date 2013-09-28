from . import abstract_wrappers


class PyPIWrapper(abstract_wrappers.AbstractJsonApiWrapper):
    base_url = 'http://pypi.python.org/pypi'

    def package_info(self, name, version=None):
        self.hammock = self.hammock(name)
        if version:
            self.hammock = self.hammock(version)
        self.hammock = self.hammock.json
        return 'GET', {}
