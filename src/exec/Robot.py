
from flockbot import FlockBot
import struct
import math

rotSpeed = 10
moveSpeed = 10
calib = {1:100,2:100}
directions = ['N', 'E', 'S', 'W']

class Robot(FlockBot):
    
    def __init__(self, number, board):
        super(Robot, self).__init__('10.0.0.3{}'.format(number))
        self.board = board
        self.id = number
        self.parser['LO'] = lambda (msg) : struct.unpack('=2sbbc', msg)
        self.actionComplete = False
        self.foundSquare = False
        
    def update(self):
        msg = self.read()
        while not msg == None:
            if msg[0] == 'AC':
                self.actionComplete = True
            elif msg[0] == 'LO':
                self.foundSquare = True
                self.pos = (msg[1], msg[2], msg[3])
                sefl.board.setRobot(self.id, self.pos)
    
    def setDirection(self, dir):
        if not self.actionComplete and not self.foundSquare:
            print "Cannot set direction, other actions in progress"
        self.actionComplete = False
        self.foundSquare = False
        cur = self.pos[2]
        curIdx = directions.index(cur) + 1
        nextIdx = directions.index(dir) + 1
        
        if curIdx - nextIdx == -1:
            self.roate(rotSpeed, 90)
        elif curIdx - nextIdx == 1:
            self.roate(rotSpeed, -90)
        elif math.fabs((curIdx - nextIdx)) == 2:
            self.roate(rotSpeed, 180)
        elif curIdx - nextIdx == 3:
            self.roate(rotSpeed, 90)
        elif curIdx - nextIdx == 4:
            self.roate(rotSpeed, -90)
            
    def forward(self):
        if not self.actionComplete and not self.foundSquare:
            print "Cannot move forward, other actions in progress"
        self.actionComplete = False
        self.foundSquare = False
        self.moveDistance(moveSpeed, calib[self.id])