from flockbot import FlockBot
import struct
import math

rotSpeed = {0:15, 5:15, 8:15}
moveSpeed = {0:20, 5:18, 8:21}
moveDist = {0:30, 1:30, 2:30, 3:30, 5:30, 6:30, 8:30}
fpushDist = {0:40, 5:40, 8:40}
bpushDist = {0:10, 5:10, 8:10}
initPos = {0:((0,0),'n'), 5:((3,3),'s')}
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
        print 'R-', self.id, ' Doing ', a
        self.action = a
    
    def run(self):
        if not self.action == None:
            if self.actionComplete:
                if 'move' == self.action[0]:
                    self.move()
                elif 'push' == self.action[0]:
                    self.push()
            
    def update(self):
        self.board.setRobot(self.id, self.pos)
        msg = self.read()
        while not msg == None:
            if msg[0] == 'DMC':
                self.actionComplete = True
                self.pos = self.next_pos
                if 'push' == self.action[0] and self.pushState == 2:
                    self.pushState = 3
            print self.actionComplete,  msg
            msg = self.read()

    def completed(self):
        if not self.action == None:
            if 'move' == self.action[0]:
                return self.pos[0] == self.action[2]
            elif 'push' == self.action[0]:
                if self.pos[0] == self.action[2] and self.pushState == 3:
                    self.pushState = 0
                    self.action = None
                    return True
                else:
                    return False
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
    
    def push(self):
        (action, current, next, dir) = self.action
        print 'pushing to ', next, dir, self.pushState
        print 'At ', self.pos
        if self.pos[0] == current:
            if self.pushState == 0:
                if self._checkAction('push box', 'push'):
                    if self.pos[1] == dir:
                        self.next_pos = self.compute_next_pos(dir)
                        self.moveDistance(moveSpeed[self.id], fpushDist[self.id])
                        self.pushState = 1
                    else:
                        self.next_pos = (self.pos[0], dir)
                        self.setDirection(dir)
        elif self.pushState == 1:
            self.pushState = 2
            self.board.pushBox(next, dir)
            self.moveDistance(-1*moveSpeed[self.id], bpushDist[self.id])
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
            return 90
        elif n == 1:
            return -90
        elif n == 2:
            return 180
        elif n == 0:
            return 0
        else:
            print 'Unknown ', curIdx, nextIdx, (curIdx - nextIdx)
        return None
        
    def setDirection(self, dir):
        self.actionComplete = False
        deg = self.getDegrees(dir)
        print 'R-', self.id, ' rotating ', deg
        if deg < 0:
            self.rotate(-1*rotSpeed[self.id], -1*deg)
        else:
            self.rotate(rotSpeed[self.id], deg)
        
    def _checkAction(self, msg, type):
        if type == 'move':
            if self.board.isOpen(self.action[2]):
                self.actionComplete = False
                return True
        elif type == 'push':
            print self.action, ' in ', self.board.box
            if type == 'push' and not self.action[2] in self.board.box:
                print 'next space no box'
                return False
            self.actionComplete = False
            return True