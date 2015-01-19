# -*- coding: utf-8 -*-


from thriftpy.protocol import TCyBinaryProtocolFactory
from thriftpy.thrift import TClient
from thriftpy.transport import (
    TCyBufferedTransportFactory,
    TSocket)

PROTO_FACTORY = TCyBinaryProtocolFactory
TRANS_FACTORY = TCyBufferedTransportFactory


def make_client(service, host, port, timeout=None):
    """

    :param service: thrift service type instance
    :param timeout: seconds after which the client would expire
    :return: a client proxy instance that can call the remote api
    directly, without using a context directly
    """
    if timeout is None:
        timeout = 120 * 1000
    return ClientProxy(service, host, port, timeout)


def _wrapper_api(api, transport):
    def wrapper(*args, **kwargs):
        try:
            transport.open()
            return api(*args, **kwargs)
        finally:
            transport.close()

    return wrapper


class ClientProxy(object):
    def __init__(self, service, host, port, timeout):
        self.service = service
        self.host = host
        self.port = port
        self.timeout = timeout

    def __getattr__(self, item):
        socket = TSocket(self.host, self.port)
        socket.set_timeout(self.timeout)
        transport = TRANS_FACTORY().get_transport(socket)
        protocol = PROTO_FACTORY().get_protocol(transport)
        client = TClient(self.service, protocol)
        attr = getattr(client, item)
        return _wrapper_api(attr, transport)
