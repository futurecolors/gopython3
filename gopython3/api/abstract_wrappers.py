from hammock import Hammock


class AbstractJsonApiWrapper(object):
    """ Abstract class for all API wrappers"""
    base_url = None
    api_methods_prefix = 'ask_about'

    def __init__(self):
        self._reset_hammock()

    def __getattr__(self, item):
        if item.startswith(self.api_methods_prefix):
            name = item[len(self.api_methods_prefix) + 1:]
            return self.make_request(name)

    def get_common_request_kwargs(self):
        return {
            'proxies': {},
        }

    def make_request(self, call_slug):
        """ Returns all info about something from API"""
        def make_request_with_kwargs(**kwargs):
            request_method, additional_request_kwargs = getattr(self, call_slug)(**kwargs)
            request_kwargs = self.get_common_request_kwargs()
            for k, v in additional_request_kwargs.items():
                if k in request_kwargs and type(v) is dict:  # not overriding sub-dicts
                    request_kwargs[k].update(v)
                else:
                    request_kwargs[k] = v
            response = getattr(self.hammock, request_method)(**request_kwargs)
            self._reset_hammock()
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        return make_request_with_kwargs

    def _reset_hammock(self):
        self.hammock = Hammock(self.base_url)

    # def example_api_method(self, some_name):
    #     """ Example of concrete API method.
    #         Should edit self.hammock to appropriate path.
    #         Should return request method and request params.
    #         Should be called as wrapper.ask_about_example_api_method(**kwargs) [see self.api_method_prefix].
    #         When called, all params should be kwargs.
    #     """
    #     self.hammock = self.hammock.blah.blah
    #     return 'GET', {}


class AbstractJsonApiWrapperWithAuth(AbstractJsonApiWrapper):
    """ API wrapper with authorisation support."""
    def get_credentials(self):
        """ Auth data in GET params"""
        return {}

    def header_credentials(self):
        """ Auth data in request headers"""
        return {}

    def get_common_request_kwargs(self):
        kwargs = super(AbstractJsonApiWrapperWithAuth, self).get_common_request_kwargs()
        kwargs.update({
            'params': self.get_credentials(),
            'headers': self.header_credentials(),
        })
        print('auth', kwargs)
        return kwargs
