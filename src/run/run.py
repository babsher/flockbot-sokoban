from robot import Robot
from board import Board
import re
import time
import zerorpc

PLAN = True
robotId = [3, 6]
dirMap = {'dir-south': 'S', 'dir-north': 'N', 'dir-west': 'W', 'dir-east':'E'}

def getPos(m, g1, g2):
    return (int(m.group(g1)), int(m.group(g2)))

def getPlan(file):
    out = {}
    for r in robotId:
        out[r] = []
    
    #                    move robot to from dir
    move = re.compile('\(move robot-(\d) pos-(\d)-(\d) pos-(\d)-(\d) (dir-\w+)\)')
    #                    push-to-goal robot box  from to dir
    push = re.compile('\(push-to-(non)?goal robot-(\d) stone-\d+ pos-(\d)-(\d) pos-(\d)-(\d) pos-(\d)-(\d) (dir-\w+)\)')
    for line in open(file, 'r').readlines():
        m = move.match(line)
        if m:
            out[int(m.group(1))].append(('move', getPos(m, 2, 3), getPos(m, 4, 5), dirMap[m.group(6)]))
        m = push.match(line)
        if m:
            out[int(m.group(2))].append(('push', getPos(m, 3, 4), getPos(m, 5, 6), dirMap[m.groupd()]))
    return out

if __name__ == "__main__":
    board = Board()
    robots = [Robot(x, board) for x in robotId]
    
    print 'Connecting to robots ', robotId
    for r in robots:
        r.connect()
        r.testConnection()
    
    # get grid
    # get robot pos
    bird = zerorpc.Client()
    bird.connect("tcp://10.0.0.106:4242")
    # plan
    
    # Select parts for this robot
    plan = getPlan('./src/simple.pddl.soln')
    print plan
    
    # TODO Identify preconditions for this robots steps
    # while has steps not completed
    done = False
    while not done:
        for r in robots:
            r.update()
            if r.actionComplete:
                curr = plan[r.id][0]
                print 'current move ', curr
                if r.completed(curr):
                    print 'Moving ', curr, ' competed'
                    plan[r.id].remove(curr)
                    curr = plan[r.id][0]
                if 'move' == curr[0]:
                    r.move(curr[1], curr[2], curr[3])
        time.sleep(1)
    
    #   check precondition of step
    #   start timeout
    #   if timeout replan
    #   if precondition run step
    
    
