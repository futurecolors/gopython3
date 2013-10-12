# coding: utf-8


class APIError(Exception):
    pass


class RateLimitExceeded(APIError):
    pass
