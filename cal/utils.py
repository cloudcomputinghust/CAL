import datetime
try:
    import simplejson as json
except ImportError:
    import json
import random

import falcon
from falcon import Response

import cal.conf

CONF = cal.conf.CONF


class JSONRequestDeserializer(object):

    def has_body(self, request):
        if 'transfer-encoding' in request.headers:
            return True
        elif request.content_length > 0:
            return True

        return False

    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.loads."""
        return obj

    def from_json(self, datastring):
        try:
            return json.loads(datastring, object_hook=self._sanitizer)
        except ValueError:
            msg = 'Malformed JSON in request body.'
            raise falcon.HTTPBadRequest(
                title='Malformed JSON', description=msg)

    def default(self, request):
        if self.has_body(request):
            body = request.stream.read(request.content_length)
            return {'body': self.from_json(body.decode("utf-8"))}
        else:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON doc is required')


class JSONResponseSerializer(object):

    def _sanitizer(self, obj):
        """Sanitizer method that will be passed to json.dumps."""
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return obj

    def to_json(self, data):
        return json.dumps(data, default=self._sanitizer, sort_keys=True)

    def default(self, response, result):
        response.content_type = 'application/json'
        response.body = self.to_json(result)


def append_request_id(req, resp, resource, params):
    """Append request id which got from response
    header to resource.req_ids list.
    """
    def get_headers(resp):
        if hasattr(resp, 'headers'):
            return resp.headers
        if hasattr(resp, '_headers'):
            return resp._headers
        return None

    if(isinstance(resp, Response) or
       (get_headers(resp) is not None)):
        # Extract 'x-request-id' from headers if
        # response is a Response object.
        request_id = get_headers(resp).get('x-request-id')
    else:
        # If resp is of type string or None.
        request_id = resp

    if resource.req_ids is None:
        resource.req_ids = []

    if request_id not in resource.req_ids:
        resource.req_ids.append(request_id)


def pick_cloud_provider():
    # Random pick one cloud provider.
    provider = list(CONF.providers.driver_mapper.keys())
    return random.choice(provider)


def pick_host_with_specific_provider(provider, cloud_config=None):
    if cloud_config is None:
        hosts = getattr(CONF, provider.lower())['hosts']
        # Now, random choice host from provider hosts.
        # TODO(kiennt): Next phase, pick the most optimized host
        #               of given provider.
        picked_host_config = hosts[random.choice(list(hosts.keys()))]
        return picked_host_config
    else:
        # TODO(kiennt): Check this cloud config: raise Exception
        #               if the given config is invalid (Must be a
        #               dict with the same keys like the one in
        #               conf/providers.py), or connection to this
        #               host is refused, broken...
        return cloud_config
