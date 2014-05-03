from Queue import Queue
import thread
import socket
from select import select
import struct

HOST = '10.0.0.31'
PORT = 2005
DEBUG = True

def getHex(msg):
    return ':'.join(x.encode('hex') for x in msg)

class FlockBot():

    def __init__(self, host):
        self.host = host
        self.port = 2005
        self.parser = {
            'AC' : lambda (msg) : struct.unpack('=3s', msg),
            'SP' : lambda (msg) : struct.unpack('=2shhhhhh??hhhhh2s', msg),
            'DM' : lambda (msg) : struct.unpack('=3s', msg)
        }
        
    def _connect(self, sock, send, recv):
        print 'Running!'
        length = None
        msg = ''
        while self.running:
            ready = select([sock], [], [], 1)
            if ready[0]:
                if length is None:
                    d = sock.recv(1)
                    if len(d) > 0:
                        length = struct.unpack('b', d[0])[0]
                        if DEBUG:
                            print 'Got packet of {} bytes.'.format(length)
                        if len(d) > 1:
                            msg = d[1:]
                elif len(msg) < length:
                    chunk = sock.recv(length-len(msg))
                    print chunk
                    msg = msg + chunk
                if len(msg) == length:
                    if DEBUG:
                        print 'Message: {}'.format(getHex(msg))
                    code = struct.unpack('2s', msg[:2])[0]
                    if DEBUG:
                        print 'Got code: {}'.format(code)
                    msg = self.parser.get(code)(msg)
                    if msg:
                        recv.put(msg)
                    length = None
                    msg = ''
            if not send.empty():
                sock.send(send.get(False))
        print 'Shutting down, good bye.'
        sock.close()
        
    def connect(self):
        for res in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                sock = socket.socket(af, socktype, proto)
            except socket.error as msg:
                sock = None
                continue
            try:
                sock.connect(sa)
                sock.setblocking(0)
            except socket.error as msg:
                sock.close()
                sock = None
                continue
            break
        if not sock == None:
            self.recv = Queue(1024)
            self.send = Queue(1024)
            self.running = True
            self.thread = thread.start_new_thread(self._connect, (sock, self.send, self.recv))
        else:
            print msg

    def close(self):
        self.running = False

    def read(self):
        if not self.recv.empty():
            return self.recv.get(False)
        return None
    
    def read_block(self):
        return self.recv.get(True, 99999)
    
    def testConnection(self):
        self.send.put('hello')
        self.read_block()
        
    def registerSensors(self, rate):
        msg = struct.pack('<b2si', 6, 'SS', rate)
        self.send.put(msg)
        
    def stopSensor(self):
        msg = struct.pack('<b2s', 6, 'SF', rate)
        self.send.put(msg) 
        
    def closeClaw(self):
        msg = struct.pack('<b2sb3s', 6, 'RT', 3, 'DGC')
        self.send.put(msg)
    
    def openClaw(self):
        msg = struct.pack('<b2sb3s', 6, 'RT', 3, 'DGO')
        self.send.put(msg)
    
    def moveSpeed(self, speed):
        msg = struct.pack('=b2sb3sb', 7, 'RT', 4, 'DMS', speed)
        self.send.put(msg)
    
    def moveDistance(self, speed, dist):
        msg = struct.pack('<b2sb3sbH', 9, 'RT', 6, 'DMD', speed, dist)
        if DEBUG:
            print 'sending move: {} '.format(repr(msg))
        self.send.put(msg)
        
    def moveWheels(self, left, right):
        msg = struct.pack('<b2sb3sbb', 8, 'RT', 5, 'DMW', left, right)
        self.send.put(msg)
        
    def rotate(self, speed):
        msg = struct.pack('<b2sb3sb', 7, 'RT', 4, 'DRC', speed)
        self.sock.send(msg)
        
    def rotate(self, speed, deg):
        msg = struct.pack('<b2sb3sbh', 9, 'RT', 6, 'DRD', speed, deg)
        if DEBUG:
            print 'sending rot: {} '.format(':'.join(x.encode('hex') for x in msg))
        self.send.put(msg)
        
    def stop(self):
        msg = struct.pack('<b2s', 2, 'ST')
        self.send.put(msg)
