class Board:
    
    def _init_(self):
        self.robots = {}
        self.blocks = []
    
    def setRobot(self, r, pos):
        self.robots[r] = pos
    
    def setBlocks(self, blocks):
        self.blocks = blocks