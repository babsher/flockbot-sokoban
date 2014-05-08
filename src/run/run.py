from robot import Robot
from board import Board
from createPDDL import *
import re
import time
from sets import Set
from subprocess import call
import threading
import signal

stop = threading.Event()

BIRD_IP = "tcp://10.0.0.110:4242"

MAX_X = 3
MAX_Y = 1

PLAN = False
RUN_ROBOTS = False

robotId = [0]
dirMap = {'dir-south': 's', 'dir-north': 'n', 'dir-west': 'w', 'dir-east':'e'}

def getPos(m, g1, g2):
    return (int(m.group(g1)), int(m.group(g2)))

def getPlan(file):
    out = {}
    for r in robotId:
        out[r] = []
    
    #                    move robot to from dir
    move = re.compile('\(move robot-(\d) pos-(\d)-(\d) pos-(\d)-(\d) (dir-\w+)\)')
    #                    push-to-goal robot box from to dir
    push = re.compile('\(push-to-(non)?goal robot-(\d) stone-\d+ pos-(\d)-(\d) pos-(\d)-(\d) pos-(\d)-(\d) (dir-\w+)\)')
    for line in open(file, 'r').readlines():
        m = move.match(line)
        if m:
            out[int(m.group(1))].append(('move', getPos(m, 2, 3), getPos(m, 4, 5), dirMap[m.group(6)]))
        m = push.match(line)
        if m:
            out[int(m.group(2))].append(('push', getPos(m, 3, 4), getPos(m, 5, 6), dirMap[m.groupd()]))
    return out

def mainLoop():
    # get grid
    board = Board(BIRD_IP, MAX_X, MAX_Y)
    robots = [Robot(x, board) for x in robotId]
    
    if PLAN:
        board.update()
    # get robot pos
    if RUN_ROBOTS:
        print 'Connecting to robots ', robotId
        for r in robots:
            r.connect()
            r.testConnection()
            while r.pos == None:
                r.update()
            print 'Robot {} starting at {}'.format(r.id, r.pos)
    
    # plan
    if PLAN:
        # write problem
        pddl = makePDDL(board.positions, board.robots, board.blocked, board.box, board.goal)
        f = open('problem.pddl', 'w')
        f.write(pddl)
        f.close()
        call(['/usr/local/bin/python3', './src/pyperplan.py', './domain.pddl', './problem.pddl'])
    
    # Select parts for this robot
    plan = getPlan('./src/simple.pddl.soln')
    print plan
    

    # while has steps not completed
    while not stop.is_set():
        for r in robots:
            r.update()
            if r.actionComplete:
                if len(plan[r.id]) > 0:
                    if r.completed(): # go to next move if robot is ready
                        curr = plan[r.id].pop(0)
                        print 'Moving ', curr, ' competed'
                        r.do(curr)
            r.run()
        time.sleep(1)
    #   check precondition of step
    #   start timeout
    #   if timeout replan
    #   if precondition run step
    for r in robots:
        r.close()

if __name__ == "__main__":
    t = threading.Thread(target=mainLoop)
    t.start()
    raw_input("press any button to kill...")
    stop.set()
    print 'Trying to shutdown'
    t.join()