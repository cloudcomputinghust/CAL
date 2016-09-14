import falcon
import logging
import importlib

import cal.conf

LOG = logging.getLogger(__name__)
CONF = cal.conf.CONF


class Request(falcon.Request):
    pass


class Response(falcon.Response):
    pass


class BaseMiddleware(object):

    def process_request(self, req, resp):
        """Process the request before routing it.

        Args:
            req: Request object that will eventually be
                routed to an on_* responder method.
            resp: Response object that will be routed to
                the on_* responder.
        """
        pass

    def process_resource(self, req, resp, resource, params):
        """Process the request after routing.

        Note:
            This method is only called when the request matches
            a route to a resource.

        Args:
            req: Request object that will be passed to the
                routed responder.
            resp: Response object that will be passed to the
                responder.
            resource: Resource object to which the request was
                routed.
            params: A dict-like object representing any additional
                params derived from the route's URI template fields,
                that will be passed to the resource's responder
                method as keyword arguments.
        """
        pass

    def process_response(self, req, resp, resource):
        """Post-processing of the response (after routing).

        Args:
            req: Request object.
            resp: Response object.
            resource: Resource object to which the request was
                routed. May be None if no route was found
                for the request.
        """
        pass


class BaseResource(object):
    """Base class for CAL resources"""

    def __init__(self, controller, *args, **kwargs):
        self.controller = controller
        self.req_ids = None

    def on_get(self, req, resp, *args, **kwargs):
        pass

    def on_post(self, req, resp, *args, **kwargs):
        pass

    def on_put(self, req, resp, *args, **kwargs):
        pass

    def on_delete(self, req, resp, *args, **kwargs):
        pass


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called. """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args,
                                                                  **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    pass


class BaseClient(Singleton):
    """Base Client
    :params path: module path of driver, for e.x: 'cal.v1.network.driver'
    :params provider: provider for e.x: 'OpenStack'
    :params cloud_config:
    """
    def __init__(self, path, provider, cloud_config):
        self.driver = None
        self.set_driver(path, provider, cloud_config)

    def set_driver(self, path, provider, cloud_config):
        _provider = provider.lower()
        module = importlib.import_module(path + '.' + _provider)
        LOG.info('Use %s driver for client', _provider)
        _driver = CONF.providers.driver_mapper[_provider]
        self.driver = getattr(module, _driver)(cloud_config)
