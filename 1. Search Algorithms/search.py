# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    
    lifo = util.Stack()
    exploredEdges = []

    for leaf in problem.getSuccessors(problem.getStartState()):
        lifo.push((leaf, [leaf[1]]))
    exploredEdges.append(problem.getStartState())

    if problem.isGoalState(problem.getStartState()):
        result = problem.getStartState()
        finalPath = result[1]
        return finalPath

    else:
        while (not lifo.isEmpty()):
            edges, current_path = lifo.pop()
            if edges[0] not in exploredEdges:
                exploredEdges.append(edges[0])
                for leaf in problem.getSuccessors(edges[0]):
                    if problem.isGoalState(leaf[0]):
                        finalPath = current_path[:]
                        finalPath.append(leaf[1])
                        return finalPath
                    else:
                        newPath = current_path[:]
                        newPath.append(leaf[1])
                        lifo.push((leaf, newPath))
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    fifo = util.Queue()
    exploredEdges = []

    for leaf in problem.getSuccessors(problem.getStartState()):
        print problem.getStartState()
        print leaf
        fifo.push((leaf, [leaf[1]]))
    exploredEdges.append(problem.getStartState())

    if problem.isGoalState(problem.getStartState()):
        result = problem.getStartState()
        finalPath = result[1]
        return finalPath

    else:
        while (not fifo.isEmpty()):
            edges, current_path = fifo.pop()
            if edges[0] not in exploredEdges:
                exploredEdges.append(edges[0])
                if problem.isGoalState(edges[0]):
                    finalPath = current_path[:]
                    return finalPath
                for leaf in problem.getSuccessors(edges[0]):
                    newPath = current_path[:]
                    newPath.append(leaf[1])
                    fifo.push((leaf, newPath))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priority = util.PriorityQueue()
    explored = []
    startState = problem.getStartState()

    new_tuple = (startState, [], 0)
    currentState = new_tuple[0]
    currentDirection = new_tuple[1]
    cost = new_tuple[2]

    priority.push(new_tuple, cost)

    while (1):
        new_state = priority.pop()

        if problem.isGoalState(new_state[0]):
            return new_state[1]

        if new_state[0] not in explored:
            explored.append(new_state[0])
            new_cost = new_state[2]
            for next in problem.getSuccessors(new_state[0]):
                cost = new_cost
                path = new_state[1]
                path = path + [next[1]]
                cost += next[2]
               
                priority.push((next[0], path, cost), cost)
                
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    priority = util.PriorityQueue()
    explored = []
    startState = problem.getStartState()
    h_function = heuristic(startState, problem)
    g_function = 0
    heuristic_function = h_function + g_function

    new_tuple = (startState,[], 0)
    currentState = new_tuple[0]
    currentDirection = new_tuple[1]
    cost = new_tuple[2]

    priority.push(new_tuple, h_function)

    while (not priority.isEmpty()):
        new_state = priority.pop()
 
        if problem.isGoalState(new_state[0]):
            return new_state[1]
 
        if new_state[0] not in explored:
            explored.append(new_state[0])
            new_cost = new_state[2]
            for next in problem.getSuccessors(new_state[0]):
                cost = new_cost
                path = new_state[1]
                path = path + [next[1]]
                g_function = next[2] + cost
                h_function = heuristic(next[0], problem)
                heuristic_function = h_function + g_function
 
                priority.push((next[0], path, g_function), heuristic_function)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
