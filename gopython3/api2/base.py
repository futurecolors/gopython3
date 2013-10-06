# coding: utf-8
from hammock import Hammock


class HammockAPI(object):
    base_url = None

    def __init__(self, *args, **kwargs):
        self.api = Hammock(self.base_url, params=self.params(), headers=self.headers())

    def params(self):
        return {}

    def headers(self):
        return {}


def is_py3_topic(*args):
    PYTHON_3_KEYWORDS = (
        'Python 3',
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
