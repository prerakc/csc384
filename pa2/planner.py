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

    ### END OF IMPLEMENTATION ###
    
    return 0

def weighted_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of weighted a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    ### IMPLEMENT BELOW ###

    ### END OF IMPLEMENTATION ###

    return False

def iterative_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of iterative a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    # HINT: Use os.times()[0] to obtain the clock time. Your code should finish within the timebound.'''
    
    ### IMPLEMENT BELOW ###

    ### END OF IMPLEMENTATION ###

    return False

def heur_alternate(state):

    '''a better warehouse heuristic'''
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
  
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.
    
    ### IMPLEMENT BELOW ###

    ### END OF IMPLEMENTATION ###
    
    return 0

