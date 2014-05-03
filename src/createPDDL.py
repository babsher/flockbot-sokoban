#! /usr/bin/python

import sys
import re
from sets import Set

filename = sys.argv[1]
outFilename = sys.argv[2]
print 'Generating problem for file: {}'.format(filename)
print 'Writing to file: {}'.format(outFilename)

file = open(filename)
out = open(outFilename, 'w')

robot = {}
open = set()
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
                open.add((col, row))
            elif entry == 'B':
                box.add((col, row))
            elif entry == 'E':
                goal.add((col, row))
            else:
                print 'Unknown: {}'.format(entry)
            col += 1
    row += 1

positions = set(robot.keys()) | blocked | box | goal | open

def printPat(keys, pat):
    for pos in keys:
        out.write(pat.format(pos))

def printLoc(keys):
    printPat(keys, "    pos-{0[0]}-{0[1]} - location\n")
    
def printNonGoal(keys):
    printPat(keys, "    (IS-NONGOAL pos-{0[0]}-{0[1]})\n")

def printMoves(keys):
    for key in keys:
        if not key in blocked:
            up = (key[0],key[1]-1)
            down = (key[0], key[1]+1)
            left = (key[0]-1, key[1])
            right = (key[0]+1, key[1])
            if (not up in blocked) and (up in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-north)\n'.format(key, up))
            if (not down in blocked) and (down in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-south)\n'.format(key, down))
            if (not left in blocked) and (left in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-west)\n'.format(key, left))
            if (not right in blocked) and (right in positions):
                out.write('    (MOVE-DIR pos-{0[0]}-{0[1]} pos-{1[0]}-{1[1]} dir-east)\n'.format(key, right))

out.write("(define (problem p012-microban-sequential)\n  (:domain sokoban-sequential)\n  (:objects\n")
out.write("    dir-south - direction\n")
out.write("    dir-east - direction\n")
out.write("    dir-west - direction\n")
out.write("    dir-north - direction\n")

i = 0
for r in robot.items():
    out.write("    {0[1]} - player\n".format(r))
i = 0
for b in box:
    i = i + 1
    out.write("    stone-{:0>2} - stone\n".format(i))

printLoc(robot)
printLoc(box)
printLoc(open)
printLoc(goal)

out.write("  )  \n(:init\n")

printPat(goal, "    (IS-GOAL pos-{0[0]}-{0[1]})\n")
printNonGoal(robot)
printNonGoal(box)
printNonGoal(open)

printMoves(positions)

i = 0
for b in box:
    i = i + 1
    out.write("    (at stone-{0:0>2} pos-{1[0]}-{1[1]})\n".format(i, b))

for p in positions - blocked - box:
    out.write("    (clear pos-{0[0]}-{0[1]})\n".format(p))
        
for (k, r) in robot.items():
    out.write("    (at {0} pos-{1[0]}-{1[1]})\n".format(r, k))

out.write('  )\n  (:goal (and\n')

i = 0
for b in box:
    i = i + 1
    out.write("    (at-goal stone-{:0>2})\n".format(i))
out.write('    )\n  )\n)'.format())