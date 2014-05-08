from flockbot import FlockBot
import struct
import math

rotSpeed = {0:15}
moveSpeed = {0:20}
moveDist = {0:30, 1:30, 2:30, 3:30, 5:30, 6:30, 9:30}
fpushDist = {0:45}
bpushDist = {0:7}
initPos = {0:((8,3),'n')}
directions = ['n', 'e', 's', 'w']

class Robot(FlockBot):
    
    def __init__(self, number, board):
        FlockBot.__init__(self, '10.0.0.3{}'.format(number))
        self.board = board
        self.id = number
        self.parser['LO'] = lambda (msg) : struct.unpack('=2sbbc', msg)
        self.actionComplete = True
        self.pos = initPos[self.id]
        self.pushState = 0
        self.action = None
        
    def do(self, a):
        print 'Doing ', a
        self.action = a
    
    def run(self):
        if not self.action == None:
            if self.actionComplete:
                if 'move' == self.action[0]:
                    self.move()
                elif 'push' == self.action[0]:
                    self.push()
                self.actionComplete = False
            
    def update(self):
        self.board.setRobot(self.id, self.pos)
        msg = self.read()
        while not msg == None:
            if msg[0] == 'DMC':
                self.actionComplete = True
                self.pos = self.next_pos
            print self.actionComplete,  msg
            msg = self.read()

    def completed(self):
        if not self.action == None:
            if 'move' == self.action[0]:
                return self.pos[0] == self.action[2]
            elif 'push' == self.action[0]:
                return self.pos[0] == self.action[2] and self.pushState == 1
        return True
        
    def compute_next_pos(self, dir):
        loc = self.pos[0]
        if dir == 'w':
            return ((loc[0]-1, loc[1]), self.pos[1])
        elif dir  == 'e':
            return ((loc[0]+1, loc[1]), self.pos[1])
        elif dir  == 'n':
            return ((loc[0], loc[1]+1), self.pos[1])
        elif dir  == 's':
            return ((loc[0], loc[1]-1), self.pos[1])
                
    def move(self):
        (action, current, next, dir) = self.action
        print 'Moving to ', next, dir
        print 'At ', self.pos
        if self.pos[0] == current:
            if self.pos[1] == dir:
                if self._checkAction('move forward', 'move'):
                    self.next_pos = self.compute_next_pos(dir)
                    self.moveDistance(moveSpeed[self.id], moveDist[self.id])
            else:
                self.next_pos = (self.pos[0], dir)
                self.setDirection(dir)
        else:
            print 'Preconditions not met for move'
    
    def push(self, box, current, next, dir):
        print 'pushing to ', next, dir
        print 'At ', self.pos
        if self.pos[0] == current:
            if self.pos[1] == dir and self.pushState == 0:
                if self._checkAction('move forward', 'push'):
                    self.next_pos = self.compute_next_pos(dir)
                    self.moveDistance(moveSpeed[self.id], fpushDist[self.id])
                    self.pushState = 1
            elif self.pushState == 1:
                self.moveDistance(-1*moveSpeed[self.id], bpushDist[self.id])
            else:
                self.setDirection(dir)
        else:
            print 'Preconditions not met for move'
        
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
        deg = self.getDegrees(dir)
        self.rotate(rotSpeed[self.id], deg)
        
    def _checkAction(self, msg, type):
        # TODO check next pos is open in board
        self.actionComplete = False
        return True