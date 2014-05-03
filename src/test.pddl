(define (problem p012-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-south - direction
    dir-east - direction
    dir-west - direction
    dir-north - direction
    robot-2 - player
    robot-1 - player
    stone-01 - stone
    pos-1-2 - location
    pos-0-1 - location
    pos-0-4 - location
    pos-2-1 - location
    pos-2-0 - location
    pos-2-2 - location
    pos-1-0 - location
    pos-0-3 - location
    pos-0-2 - location
  )  
(:init
    (IS-GOAL pos-0-1)
    (IS-NONGOAL pos-1-2)
    (IS-NONGOAL pos-2-2)
    (IS-NONGOAL pos-2-1)
    (IS-NONGOAL pos-2-0)
    (IS-NONGOAL pos-0-4)
    (IS-NONGOAL pos-1-0)
    (IS-NONGOAL pos-0-3)
    (IS-NONGOAL pos-0-2)
    (MOVE-DIR pos-1-2 pos-0-2 dir-west)
    (MOVE-DIR pos-1-2 pos-2-2 dir-east)
    (MOVE-DIR pos-0-1 pos-0-2 dir-south)
    (MOVE-DIR pos-2-2 pos-2-1 dir-north)
    (MOVE-DIR pos-2-2 pos-1-2 dir-west)
    (MOVE-DIR pos-2-1 pos-2-0 dir-north)
    (MOVE-DIR pos-2-1 pos-2-2 dir-south)
    (MOVE-DIR pos-0-2 pos-0-1 dir-north)
    (MOVE-DIR pos-0-2 pos-0-3 dir-south)
    (MOVE-DIR pos-0-2 pos-1-2 dir-east)
    (MOVE-DIR pos-2-0 pos-2-1 dir-south)
    (MOVE-DIR pos-2-0 pos-1-0 dir-west)
    (MOVE-DIR pos-0-4 pos-0-3 dir-north)
    (MOVE-DIR pos-1-0 pos-2-0 dir-east)
    (MOVE-DIR pos-0-3 pos-0-2 dir-north)
    (MOVE-DIR pos-0-3 pos-0-4 dir-south)
    (at stone-01 pos-1-2)
    (clear pos-0-1)
    (clear pos-0-4)
    (clear pos-2-1)
    (clear pos-0-2)
    (clear pos-2-0)
    (clear pos-2-2)
    (clear pos-1-0)
    (clear pos-0-3)
    (at robot-2 pos-2-0)
    (at robot-1 pos-0-4)
  )
  (:goal    (at-goal stone-01)
  )
)