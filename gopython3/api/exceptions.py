# coding: utf-8
from requests import ConnectionError


class APINotResponding(ConnectionError):
    pass


class APIRequestError(ConnectionError):
    pass


class RateLimitExceeded(ConnectionError):
    pass
