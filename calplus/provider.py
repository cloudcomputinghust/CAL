""" Define provider class
"""


class Provider(object):

    def __init__(self, type, config):
        self._type = type
        self._config = config

    @property
    def config(self):
        return self._config

    @property
    def type(self):
        return self._type
