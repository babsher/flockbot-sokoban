from robot import Robot
from board import Board
from createPDDL import *
import re
import time
import zerorpc
from sets import Set
from subprocess import call

PLAN = False
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

def getTuple(list):
    return  [(x[0],x[1]) for x in list]

def getAllPositions():
    positions = Set()
    for x in xrange(0,9):
        for y in xrange(0,8):
            positions.add((x,y))
    return positions
            

if __name__ == "__main__":
    board = Board()
    robots = [Robot(x, board) for x in robotId]
    
    # get grid
    positions = getAllPositions()
    robots = {}
    # get robot pos
    if PLAN:
        bird = zerorpc.Client()
        bird.connect("tcp://10.0.0.105:4242")
        blocked = Set(getTuple(bird.get_obs_pts()))
        box = Set(getTuple(bird.get_box_pts()))
        goal = Set(getTuple(bird.get_goal_pts()))

        print blocked, box, goal

    print 'Connecting to robots ', robotId
    for r in robots:
        r.connect()
        r.testConnection()
        while r.pos == None:
            r.update()
        robots[r.id] = r.pos
        print 'Robot {} starting at {}'.format(r.id, r.pos)
    
    # plan
    if PLAN:
        # write problem
        pddl = makePDDL(positions, robots, blocked, box, goal)
        f = open('problem.pddl', 'w')
        f.write(pddl)
        f.close()
        call(['/usr/local/bin/python3', './src/pyperplan.py', './domain.pddl', './problem.pddl'])
    
    # Select parts for this robot
    plan = getPlan('./src/simple.pddl.soln')
    print plan
    

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
                # Identify preconditions for this robots steps
                if 'move' == curr[0]:
                    r.move(curr[1], curr[2], curr[3])
                elif 'push' == curr[0]:
                    r.push(curr[1], curr[2], curr[3], curr[4])
        time.sleep(1)
    
    #   check precondition of step
    #   start timeout
    #   if timeout replan
    #   if precondition run step
    
    
