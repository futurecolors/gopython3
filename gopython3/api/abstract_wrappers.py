from hammock import Hammock


class AbstractJsonApiWrapper(object):
    """ Abstract class for all API wrappers"""
    base_url = None
    api_methods_prefix = 'ask_about'

    def __init__(self):
        self.hammock = Hammock(self.base_url)

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
            request_method, request_kwargs = getattr(self, call_slug)(**kwargs)
            request_kwargs.update(self.get_common_request_kwargs())
            response = getattr(self.hammock, request_method)(**request_kwargs)
            if response.status_code == 200:
                return response.json()
            else:
                return {}
        return make_request_with_kwargs

    # def example_api_method(self, some_name):
    #     """ Example of concrete API method.
    #         Should edit self.hammock to appropriate path.
    #         Should return request method and request params.
    #         Should be called as wrapper.ask_about_example_api_method(**kwargs) [see self.api_method_prefix].
    #         When called, all params should be kwargs.
    #     """
    #     self.hammock = self.hammock.blah.blah
    #     return 'GET', {}
