from sets import Set
import zerorpc

class Board:
    
    def __init__(self, ip, x, y):
        self.ip = ip
        self.robots = {}
        self.blocked = Set()
        self.box = Set()
        self.box.add((1,1))
        self.goal = Set()
        self.positions = self.getAllPositions(x,y)
    
    def isOpen(self, loc):
        return loc in self.positions - self.blocked - self.box - Set(self.robots.values())
    
    def getAllPositions(self, MAX_X, MAX_Y):
        positions = Set()
        for x in xrange(0,MAX_X+1):
            for y in xrange(0,MAX_Y+1):
                positions.add((x,y))
        return positions

    def getTuple(self, list):
        return  [(x[0],x[1]) for x in list]
    
    def setRobot(self, r, pos):
        self.robots[r] = pos
        
    def pushBox(self, block, dir):
        print 'Boxes ', self.box
        self.box.remove(block)
        if dir == 'w':
            self.box.add((block[0]-1, block[1]))
        elif dir == 'e':
            self.box.add((block[0]+1, block[1]))
        elif dir == 'n':
            self.box.add((block[0], block[1]+1))
        elif dir == 's':
            self.box.add((block[0], block[1]-1))
        print 'After push Boxes', self.box
    
    def setBlocks(self, blocks):
        self.blocks = blocks
    
    def getUpdates(self):
        bird = zerorpc.Client()
        bird.connect(self.ip)
        blocked = Set(self.getTuple(bird.get_obs_pts()))
        box = Set(self.getTuple(bird.get_box_pts()))
        goal = Set(self.getTuple(bird.get_goal_pts()))
        return (blocked, box, goal)
    
    def getDir(self, deg):
        if deg < 45 and deg > -45:
            return 'w'
        if deg < -45 and deg > -135:
            return 's'
        if deg > 45 and deg < 135:
            return 'n'
        return 'e'
        
    def update(self):
        (blocked, box, goal) = self.getUpdates()
        self.blocked = blocked
        self.box = box
        self.goal = goal