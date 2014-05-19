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

#BIRD_IP = "tcp://10.0.0.104:4242"
BIRD_IP = None

MAX_X = 3
MAX_Y = 5

PLAN = False
RUN_ROBOTS = True

robotId = [0, 5]
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
            out[int(m.group(1))-1].append(('move', getPos(m, 2, 3), getPos(m, 4, 5), dirMap[m.group(6)]))
        m = push.match(line)
        if m:
            out[int(m.group(2))-1].append(('push', getPos(m, 3, 4), getPos(m, 5, 6), dirMap[m.group(9)]))
    return out

def mainLoop(event):
    board = Board(BIRD_IP, MAX_X, MAX_Y)
    robots = [Robot(x, board) for x in robotId] 
    try:
        # get grid
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
                board.robots[r.pos[0]] = 'robot-{}'.format(r.id)

        # plan
        if PLAN:
            # write problem
            pddl = makePDDL(board.positions, board.robots, board.blocked, board.box, board.goal)
            f = open('problem.pddl', 'w')
            f.write(pddl)
            f.close()
            call(['/usr/local/bin/python3', './src/pyperplan.py', './domain.pddl', './problem.pddl', '-sma', '-Hhmax'])

        # Select parts for this robot
        plan = {}
        if PLAN:
            plan = getPlan('./problem.pddl.soln')
        else:
            plan =  getPlan('./src/demo.pddl.soln')
        print plan

        # while has steps not completed
        while not event.is_set():
            for r in robots:
                r.update()
                if r.actionComplete:
                    if r.completed(): # go to next move if robot is ready
                        if len(plan[r.id]) > 0:
                                curr = plan[r.id].pop(0)
                                print 'Moving ', curr
                                r.do(curr)
                r.run()
            time.sleep(1)
        #   check precondition of step
        #   start timeout
        #   if timeout replan
        #   if precondition run step
    except:
        raise
    else:
        for r in robots:
            print 'Shutting down ', r.id
            r.close()
    
def handler(signum, frame):
    global stiop
    stop.set()
    print('Signal handler called with signal [%s]' % signum)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    t = threading.Thread(target=mainLoop, args=(stop,))
    t.start()
    raw_input("press any button to kill...")
    stop.set()
    print 'Trying to shutdown'
    t.join()