#! /usr/bin/python

import sys
import re
from sets import Set

def parse(filename):
    "Parses a soko file"
    file = open(filename)

    robot = {}
    o = set()
    blocked = set()
    box = set()
    goal = set()

    row = 0
    col = 0
    lines = file.readlines()
    for line in lines:
        col = 0
        entries = re.split('\s+', line)
        for entry in entries:
            if entry != '':
                print '{0} at ({1},{2})'.format(entry, col, row)
                entry = entry.upper()
                m = re.match('(\d)', entry)
                if entry == '#' or entry == 'X':
                    blocked.add((col, row))
                elif m:
                    robot[(col, row)] = 'robot-{}'.format(m.group(0))
                elif entry == 'O':
                    o.add((col, row))
                elif entry == 'B':
                    box.add((col, row))
                elif entry == 'E':
                    goal.add((col, row))
                else:
                    print 'Unknown: {}'.format(entry)
                col += 1
        row += 1
    positions = set(robot.keys()) | box | goal | o
    return (positions, robot, blocked, box, goal)

def printPat(keys, pat, out):
    for pos in keys:
        out.append(pat.format(pos))

def printLoc(keys, out):
    printPat(keys, "    pos-{0[0]}-{0[1]} - location\n", out)
    
def printNonGoal(keys, out):
    printPat(keys, "    (IS-NONGOAL pos-{0[0]}-{0[1]})\n", out)

def printMoves(positions, blocked, out):
    for key in positions:
        if not key in blocked:
            up = (key[0],key[1]-1)
            down = (key[0], key[1]+1)
            left = (key[0]-1, key[1])
            right = (key[0]+1, key[1])
            if (not up in blocked) and (up in positions):
                out.append('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-north)\n'.format(key, up))
            if (not down in blocked) and (down in positions):
                out.append('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-south)\n'.format(key, down))
            if (not left in blocked) and (left in positions):
                out.append('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-west)\n'.format(key, left))
            if (not right in blocked) and (right in positions):
                out.append('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-east)\n'.format(key, right))

def makePDDL(positions, robot, blocked, box, goal):
    out = []
    out.append("(define (problem p012-microban-sequential)\n  (:domain sokoban-sequential)\n  (:objects\n")
    out.append("    dir-south - direction\n")
    out.append("    dir-east - direction\n")
    out.append("    dir-west - direction\n")
    out.append("    dir-north - direction\n")

    i = 0
    for r in robot.items():
        out.append("    {0[1]} - player\n".format(r))
    i = 0
    for b in box:
        i = i + 1
        out.append("    stone-{:0>2} - stone\n".format(i))

    printLoc(positions - blocked, out)

    out.append("  )  \n(:init\n")

    printPat(goal, "    (IS-GOAL pos-{0[0]}-{0[1]})\n", out)
    printNonGoal(positions - goal, out)

    printMoves(positions, blocked, out)

    i = 0
    for b in box:
        i = i + 1
        out.append("    (at stone-{0:0>2} pos-{1[0]}-{1[1]})\n".format(i, b))

    for p in positions - blocked - box:
        out.append("    (clear pos-{0[0]}-{0[1]})\n".format(p))

    for (k, r) in robot.items():
        out.append("    (at {0} pos-{1[0]}-{1[1]})\n".format(r, k))
    
    out.append('  )\n  (:goal')
    if len(box) == 1:
        out.append("    (at-goal stone-{:0>2})\n".format(i))
    else:
        out.append(' (and\n')
        i = 0
        for b in box:
            i = i + 1
            out.append("    (at-goal stone-{:0>2})\n".format(i))
        out.append('    )\n')
    out.append('  )\n)')
    return ''.join(out)

if __name__ == "__main__":
    filename = sys.argv[1]
    outFilename = sys.argv[2]
    print 'Generating problem for file: {}'.format(filename)
    
    (positions, robot, blocked, box, goal) = parse(filename)
    pddl = makePDDL(positions, robot, blocked, box, goal)
    print 'Writing to file: {}'.format(outFilename)
    out = open(outFilename, 'w')
    out.write(pddl)
    out.close()