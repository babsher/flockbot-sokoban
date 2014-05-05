import zerorpc

c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
print c.get_goal_pts()
print c.get_box_pts()