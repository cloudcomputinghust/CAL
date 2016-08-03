from oslo_context import context

from cal import base
from cal import utils


class DeserializeMiddleware(base.BaseMiddleware):

    def __init__(self):
        super(DeserializeMiddleware, self).__init__()

    def _deserialize(self, req):
        deserializer = utils.JSONRequestDeserializer()
        body = deserializer.default(req)
        cloud = body['body']['cloud']
        req.env['cal.cloud'] = str(cloud)

    def _attach_req_id_to_resp(self, req, resp):
        req_id = context.generate_request_id()
        req.env['request-id'] = req_id
        if 'x-request-id' not in resp._headers:
            resp._headers['x-request-id'] = req_id

    def process_request(self, req, resp):
        self._deserialize(req)
        self._attach_req_id_to_resp(req, resp)


class FuncMiddleware(base.BaseMiddleware):

    def __init__(self, func):
        super(FuncMiddleware, self).__init__()
        self.func = func

    def process_resource(self, req, resp, resource, params):
        return self.func(req, resp, params)


class SerializeMiddleware(base.BaseMiddleware):

    def __init__(self):
        super(SerializeMiddleware, self).__init__()

    def _serialize(self, resp, result):
        serializer = utils.JSONResponseSerializer()
        serializer.default(resp, result)

    def process_response(self, req, resp, resource, result):
        self._serialize(resp, result)
