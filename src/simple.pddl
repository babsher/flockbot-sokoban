(define (problem p012-microban-sequential)
  (:domain sokoban-sequential)
  (:objects
    dir-south - direction
    dir-east - direction
    dir-west - direction
    dir-north - direction
    robot-1 - player
    stone-01 - stone
    pos-0-1 - location
    pos-2-0 - location
    pos-0-0 - location
    pos-1-0 - location
    pos-1-1 - location
    pos-2-1 - location
  )  
(:init
    (IS-GOAL pos-0-1)
    (IS-NONGOAL pos-2-0)
    (IS-NONGOAL pos-1-0)
    (IS-NONGOAL pos-0-0)
    (IS-NONGOAL pos-1-1)
    (IS-NONGOAL pos-2-1)
    (MOVE-DIR pos-0-1 pos-0-0 dir-south)
    (MOVE-DIR pos-0-1 pos-1-1 dir-east)
    (MOVE-DIR pos-2-0 pos-2-1 dir-north)
    (MOVE-DIR pos-2-0 pos-1-0 dir-west)
    (MOVE-DIR pos-0-0 pos-0-1 dir-north)
    (MOVE-DIR pos-0-0 pos-1-0 dir-east)
    (MOVE-DIR pos-1-0 pos-1-1 dir-north)
    (MOVE-DIR pos-1-0 pos-0-0 dir-west)
    (MOVE-DIR pos-1-0 pos-2-0 dir-east)
    (MOVE-DIR pos-1-1 pos-1-0 dir-south)
    (MOVE-DIR pos-1-1 pos-0-1 dir-west)
    (MOVE-DIR pos-1-1 pos-2-1 dir-east)
    (MOVE-DIR pos-2-1 pos-2-0 dir-south)
    (MOVE-DIR pos-2-1 pos-1-1 dir-west)
    (at stone-01 pos-1-1)
    (clear pos-0-1)
    (clear pos-2-0)
    (clear pos-1-0)
    (clear pos-0-0)
    (clear pos-2-1)
    (at robot-1 pos-2-1)
  )
  (:goal    (at-goal stone-01)
  )
)