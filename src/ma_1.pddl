(define (problem p012-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-south - direction
    dir-east - direction
    dir-west - direction
    dir-north - direction
    robot-1 - player
    robot-8 - player
    stone-01 - stone
    pos-0-1 - location
    pos-3-2 - location
    pos-0-0 - location
    pos-3-3 - location
    pos-3-0 - location
    pos-2-1 - location
    pos-0-2 - location
    pos-1-3 - location
    pos-2-3 - location
    pos-2-2 - location
    pos-1-1 - location
  )  
(:init
    (IS-GOAL pos-0-2)
    (IS-NONGOAL pos-0-1)
    (IS-NONGOAL pos-3-2)
    (IS-NONGOAL pos-0-0)
    (IS-NONGOAL pos-3-3)
    (IS-NONGOAL pos-3-0)
    (IS-NONGOAL pos-2-1)
    (IS-NONGOAL pos-1-3)
    (IS-NONGOAL pos-2-3)
    (IS-NONGOAL pos-2-2)
    (IS-NONGOAL pos-1-1)
    (MOVE-DIR pos-0-1 pos-0-2 dir-north)
    (MOVE-DIR pos-0-1 pos-0-0 dir-south)
    (MOVE-DIR pos-0-1 pos-1-1 dir-east)
    (MOVE-DIR pos-3-2 pos-3-3 dir-north)
    (MOVE-DIR pos-3-2 pos-2-2 dir-west)
    (MOVE-DIR pos-0-0 pos-0-1 dir-north)
    (MOVE-DIR pos-3-3 pos-3-2 dir-south)
    (MOVE-DIR pos-3-3 pos-2-3 dir-west)
    (MOVE-DIR pos-2-1 pos-2-2 dir-north)
    (MOVE-DIR pos-2-1 pos-1-1 dir-west)
    (MOVE-DIR pos-0-2 pos-0-1 dir-south)
    (MOVE-DIR pos-1-3 pos-2-3 dir-east)
    (MOVE-DIR pos-2-3 pos-2-2 dir-south)
    (MOVE-DIR pos-2-3 pos-1-3 dir-west)
    (MOVE-DIR pos-2-3 pos-3-3 dir-east)
    (MOVE-DIR pos-2-2 pos-2-3 dir-north)
    (MOVE-DIR pos-2-2 pos-2-1 dir-south)
    (MOVE-DIR pos-2-2 pos-3-2 dir-east)
    (MOVE-DIR pos-1-1 pos-0-1 dir-west)
    (MOVE-DIR pos-1-1 pos-2-1 dir-east)
    (at stone-01 pos-1-1)
    (clear pos-0-1)
    (clear pos-3-2)
    (clear pos-0-0)
    (clear pos-3-3)
    (clear pos-3-0)
    (clear pos-2-1)
    (clear pos-1-3)
    (clear pos-2-3)
    (clear pos-2-2)
    (clear pos-0-2)
    (at robot-1 pos-0-0)
    (at robot-8 pos-2-3)
  )
  (:goal    (at-goal stone-01)
  )
)