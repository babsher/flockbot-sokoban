from nose.tools import assert_raises
import gevent
import sys

from zerorpc import zmq
import zerorpc



def test_client_server():
    endpoint = "tcp://0.0.0.0:4242"

    class MySrv(zerorpc.Server):

        def lolita(self):
            return 42

        def add(self, a, b):
            return a + b

    srv = MySrv()
    srv.bind(endpoint)
    gevent.spawn(srv.run)

    client = zerorpc.Client()
    client.connect("tcp://127.0.0.1:4242")

    print client.lolita()
    assert client.lolita() == 42

    print client.add(1, 4)
    assert client.add(1, 4) == 5

    srv.close()

test_client_server()