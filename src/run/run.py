from robot import Robot
from board import Board
import re
import time

robotId = [6]
dirMap = {'dir-south': 'S', 'dir-north': 'N', 'dir-west': 'W', 'dir-east':'E'}

def getPos(m, g1, g2):
    return (int(m.group(g1)), int(m.group(g2)))

def getPlan(file):
    out = {}
    move = re.compile('\(move robot-(\d) pos-(\d)-(\d) pos-(\d)-(\d) (dir-\w+)\)')
    for line in open(file, 'r').readlines():
        m = move.match(line)
        if m:
            out[int(m.group(1))] = [('move', getPos(m, 2, 3), getPos(m, 4, 5), dirMap[m.group(6)])]
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
    
    
