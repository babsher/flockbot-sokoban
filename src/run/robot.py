from flockbot import FlockBot
import struct
import math

rotSpeed = 10
moveSpeed = 10
calib = {1:20, 2:20, 3:2, 5:5, 6:5, 9:20}
directions = ['n', 'e', 's', 'w']

class Robot(FlockBot):
    
    def __init__(self, number, board):
        FlockBot.__init__(self, '10.0.0.3{}'.format(number))
        self.board = board
        self.id = number
        self.parser['LO'] = lambda (msg) : struct.unpack('=2sbbc', msg)
        self.actionComplete = True # TODO testing
        self.foundSquare = False
#        self.pos = ((1,1), 'W') # TODO remove
        
    def update(self):
        msg = self.read()
        while not msg == None:
            if msg[0] == 'DMC':
                self.actionComplete = True
            elif msg[0] == 'LO':
                self.foundSquare = True
                self.pos = ((msg[1], msg[2]), msg[3])
                self.board.setRobot(self.id, self.pos)
            print self.actionComplete, self.foundSquare, msg
            msg = self.read()
                
    def completed(self, action):
        if 'move' == action[0]:
            return self.pos[0] == action[2]
                
    def move(self, current, next, dir):
        print 'Moving to ', next, dir
        print 'At ', self.pos
        if self.pos[0] == current:
            if self.pos[1] == dir:
                self.forward()
            else:
                self.setDirection(dir)
        else:
            print 'Preconditions not met for move'
    
    def push(self, box, current, next, dir):
        self.move(next, current, dir)
        
    def getDegrees(self, dir):
        cur = self.pos[1]
        curIdx = 2
        nextIdx = None
        
        if cur == 'w':
            nextIdx = ['s', 'w', 'n', 'e'].index(dir) + 1
        elif cur == 'n':
            nextIdx = ['w', 'n', 'e', 's'].index(dir) + 1
        elif cur == 's':
            nextIdx = ['e', 's', 'w', 'n'].index(dir) + 1
        elif cur == 'e':
            nextIdx = ['n', 'e', 's', 'w'].index(dir) + 1
        
        n = nextIdx - curIdx
        if n == -1:
            return -90
        elif n == 1:
            return 90
        elif n == 2:
            return 180
        elif n == 0:
            return 0
        else:
            print 'Unknown ', curIdx, nextIdx, (curIdx - nextIdx)
        return None
        
    def setDirection(self, dir):
        self._checkAction('rotate')
        deg = self.getDegrees(dir)
        self.rotate(rotSpeed, deg)
            
    def forward(self):
        self._checkAction('move forward')
        self.moveDistance(moveSpeed, calib[self.id])
        
    def _checkAction(self, msg):
        if not self.actionComplete and not self.foundSquare:
            print "Cannot {}, other actions in progress".format(msg)
        self.actionComplete = False
        self.foundSquare = False # TODO remove forced true