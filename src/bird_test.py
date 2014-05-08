import zerorpc

b = zerorpc.Client()
b.connect("tcp://10.0.0.110:4242")
print b.get_flock_pts()
