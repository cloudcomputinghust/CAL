import abc
import six


@six.add_metaclass(abc.ABCMeta)
class BaseDriver(object):

    def __init__(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def create(self, configs):
        pass