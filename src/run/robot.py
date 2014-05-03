from flockbot import FlockBot
import struct
import math

rotSpeed = 10
moveSpeed = 10
calib = {1:20, 2:20, 3:2, 5:5, 6:5, 9:20}
directions = ['N', 'E', 'S', 'W']

class Robot(FlockBot):
    
    def __init__(self, number, board):
        FlockBot.__init__(self, '10.0.0.3{}'.format(number))
        self.board = board
        self.id = number
        self.parser['LO'] = lambda (msg) : struct.unpack('=2sbbc', msg)
        self.actionComplete = True # TODO testing
        self.foundSquare = True
        self.pos = ((1,1), 'W') # TODO remove
        
    def update(self):
        msg = self.read()
        while not msg == None:
            if msg[0] == 'DMC':
                self.actionComplete = True
            elif msg[0] == 'LO':
                self.foundSquare = True
                self.pos = ((msg[1], msg[2]), msg[3])
                sefl.board.setRobot(self.id, self.pos)
            self.pos = ((0,1), 'W') # TODO remove
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
    
    def setDirection(self, dir):
        self._checkAction('rotate')
        cur = self.pos[1]
        curIdx = directions.index(cur) + 1
        nextIdx = directions.index(dir) + 1
        
        if curIdx - nextIdx == -1:
            self.rotate(rotSpeed, -90)
        elif curIdx - nextIdx == 1:
            self.rotate(rotSpeed, 90)
        elif math.fabs((curIdx - nextIdx)) == 2:
            self.rotate(rotSpeed, 180)
        elif math.fabs(curIdx - nextIdx) == 3:
            self.rotate(rotSpeed, 90)
        elif curIdx - nextIdx == 4:
            self.rotate(rotSpeed, -90)
        else:
            print 'Unknown ', curIdx, nextIdx, (curIdx - nextIdx)
            
    def forward(self):
        self._checkAction('move forward')
        self.moveDistance(moveSpeed, calib[self.id])
        
    def _checkAction(self, msg):
        if not self.actionComplete and not self.foundSquare:
            print "Cannot {}, other actions in progress".format(msg)
        self.actionComplete = False
        self.foundSquare = True # TODO remove forced true