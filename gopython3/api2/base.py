# coding: utf-8
import logging
from hammock import Hammock
import requests
from .exceptions import RateLimitExceeded


logger = logging.getLogger(__name__)


class MyHammock(Hammock):
    def _request(self, method, *args, **kwargs):
        """ Process all responses

            TODO: don't use private hammock api, maybe requests callbacks/hooks?
            TODO: make this abstract method for all derived APIs to override
        """
        response = super()._request(method, *args, **kwargs)
        logger.debug('Response: %s' % response.status_code)
        logger.debug('JSON: %s' % response.json())
        if response.status_code == requests.codes.forbidden:
            # Looks like we have hit the rate limit, fail fast
            # E.g. http://developer.github.com/v3/#rate-limiting
            message = response.json().get('message', 'Generic error')
            logger.error(message)
            raise RateLimitExceeded(message)

        return response


class HammockAPI(object):
    base_url = None

    def __init__(self, *args, **kwargs):
        self.api = MyHammock(self.base_url, params=self.params(), headers=self.headers(),)


def is_py3_topic(*args):
    PYTHON_3_KEYWORDS = (
        'python 3',
        'python3',
        'py 3',
        'py3',
        'py 3k'
        'py3k'
        'python 3000',
        'python3000',
    )
    target_string = ''.join(args).lower()
    return any([keyword.lower() in target_string for keyword in PYTHON_3_KEYWORDS])
