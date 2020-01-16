# -*- coding: utf-8 -*-


class BadRequest(Exception):
    pass


class AuthenticationFailed(Exception):
    pass


class NoToken(Exception):
    pass


class DemoNotExist(Exception):
    pass
