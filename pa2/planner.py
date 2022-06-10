#Look for ### IMPLEMENT BELOW ### tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
# Search engines
from search import * 
# Warehouse specific classes
from warehouse import WarehouseState, Direction, warehouse_goal_state
# My imports
import math

def heur_displaced(state):
  '''A trivial example heuristic that is admissible'''
  '''INPUT: a warehouse state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  '''In this case, simply the number of displaced boxes.'''   
  count = 0
  for box in state.boxes:
    if box not in state.storage:
      count += 1
    return count

def heur_manhattan_distance(state):

    '''admissible heuristic: manhattan distance'''
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    ### IMPLEMENT BELOW ###

    manhattan_distance_sum = 0

    for box in state.boxes:
      smallest_manhattan_distance = math.inf

      for storage in state.storage:
        manhattan_distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])

        if manhattan_distance < smallest_manhattan_distance:
          smallest_manhattan_distance = manhattan_distance
      
      manhattan_distance_sum += smallest_manhattan_distance

    return manhattan_distance_sum

    ### END OF IMPLEMENTATION ###
    
    return 0

def weighted_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of weighted a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    ### IMPLEMENT BELOW ###

    wrap_fval_fn = lambda sN: sN.gval + weight * sN.hval

    se = SearchEngine('custom', 'full')
    se.init_search(
      initial_state,
      goal_fn=warehouse_goal_state,
      heur_fn=heuristic,
      fval_function=wrap_fval_fn
    )
    state, _ = se.search(timebound)

    return state

    ### END OF IMPLEMENTATION ###

    return False

def iterative_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of iterative a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    # HINT: Use os.times()[0] to obtain the clock time. Your code should finish within the timebound.'''
    
    ### IMPLEMENT BELOW ###

    function_start = os.times()[0]

    best_state = False
    wrap_fval_fn = lambda sN: sN.gval + weight * sN.hval

    timebound -= os.times()[0] - function_start

    while timebound > 0:
      start_time = os.times()[0]
      
      se = SearchEngine('custom', 'full')
      se.init_search(
        initial_state,
        goal_fn=warehouse_goal_state,
        heur_fn=heuristic,
        fval_function=wrap_fval_fn
      )
      state, _ = se.search(timebound)

      if not state:
        return best_state

      best_state = state
      weight = weight / 2
      timebound -= os.times()[0] - start_time
        
    return best_state

    ### END OF IMPLEMENTATION ###

    return False

def heur_alternate(state):

    '''a better warehouse heuristic'''
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
  
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    ### IMPLEMENT BELOW ###

    available_storages = state.storage - state.boxes
    boxes_left = state.boxes - state.storage

    board_corners = {
      (0, 0),
      (state.width - 1, 0),
      (0, state.height - 1),
      (state.width - 1, state.height - 1)
    }

    no_available_storages_top_edge = len([s for s in available_storages if s[1] == 0]) == 0
    no_available_storages_bottom_edge = len([s for s in available_storages if s[1] == state.height - 1])  == 0
    no_available_storages_left_edge = len([s for s in available_storages if s[0] == 0])  == 0
    no_available_storages_right_edge = len([s for s in available_storages if s[0] == state.width - 1])  == 0

    blockers = state.boxes | state.obstacles

    for box in boxes_left:
      # check if box in board corner
      if box in board_corners:
        return math.inf

      # check if box is on edge with no storages
      if (box[1] == 0 and no_available_storages_top_edge) or \
          (box[1] == state.height - 1 and no_available_storages_bottom_edge) or \
          (box[0] == 0 and no_available_storages_left_edge) or \
          (box[0] == state.width - 1 and no_available_storages_right_edge):
        return math.inf

      # check if box is cornered by edges or blockers
      up = box[1] == 0 or (box[0], box[1] - 1) in blockers
      down = box[1] == state.height - 1 or (box[0], box[1] + 1) in blockers
      left = box[0] == 0 or (box[0] - 1, box[1]) in blockers
      right = box[0] == state.width - 1 or (box[0] + 1, box[1]) in blockers

      if (up or down) and (left or right):
        return math.inf

    robot_box_manhattan_distance_sum = 0

    for robot in state.robots:
      smallest_manhattan_distance = math.inf

      for box in state.boxes:
        manhattan_distance = abs(robot[0] - box[0]) + abs(robot[1] - box[1]) - 1

        if manhattan_distance < smallest_manhattan_distance:
          smallest_manhattan_distance = manhattan_distance

      robot_box_manhattan_distance_sum += smallest_manhattan_distance

    box_storage_manhattan_distance_sum = 0

    for box in state.boxes:
      smallest_manhattan_distance = math.inf

      for storage in state.storage:
        manhattan_distance = abs(box[0] - storage[0]) + abs(box[1] - storage[1])

        if manhattan_distance < smallest_manhattan_distance:
          smallest_manhattan_distance = manhattan_distance

      box_storage_manhattan_distance_sum += smallest_manhattan_distance

    return robot_box_manhattan_distance_sum + box_storage_manhattan_distance_sum

    ### END OF IMPLEMENTATION ###
    
    return 0
