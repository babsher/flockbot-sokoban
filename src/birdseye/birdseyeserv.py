import zerorpc


class BirdseyeServ(zerorpc.Server):

	def __init__(self,grid):
		super(BirdseyeServ,self).__init__()
		self.grid = grid

	def get_box_pts(self):
		return self.grid.get_box_pts()

	def get_goal_pts(self):
		return self.grid.get_goal_pts()

	def get_obs_pts(self):
		return self.grid.get_obs_pts()