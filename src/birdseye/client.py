import zerorpc

c = zerorpc.Client()
c.connect("tcp://10.0.0.106:4242")
print c.get_goal_pts()
print c.get_box_pts()