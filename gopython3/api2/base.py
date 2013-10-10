# coding: utf-8
import logging
import datetime
from hammock import Hammock
import re
import requests
from .exceptions import RateLimitExceeded


logger = logging.getLogger(__name__)


def keep_secrets(url):
    return re.sub('(?P<name>client_secret|client_id)=[a-f0-9]+', '\g<1>=*', url)


def format_date(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')


class MyHammock(Hammock):
    def _request(self, method, *args, **kwargs):
        """ Process all responses

            TODO: don't use private hammock api, maybe requests callbacks/hooks?
            TODO: make this abstract method for all derived APIs to override
        """
        response = super()._request(method, *args, **kwargs)
        logger.info(keep_secrets(response.request.url))
        logger.debug('%s/%s Reset: %s' % (response.headers.get('X-RateLimit-Remaining'),
                                          response.headers.get('X-RateLimit-Limit'),
                                          format_date(response.headers.get('X-RateLimit-Reset', 0))
        ))
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
        self.api = MyHammock(self.base_url, params=self.params(), headers=self.headers(), )

    def params(self):
        return {}

    def headers(self):
        return {}


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
