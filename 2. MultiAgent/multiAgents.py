# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        FOOD_POINTS = 10.0
        GHOST_POINTS = -10.0

        score = successorGameState.getScore()
        ghostState = newGhostStates[0].getPosition()
        #get the manhattan distance to the ghost from pacman position
        ghostDistance = manhattanDistance(newPos, ghostState)
        if ghostDistance > 0:
            scoreSubtract = GHOST_POINTS / ghostDistance
            score = score + scoreSubtract

        foodList = newFood.asList()
        foodDistance = []
        for food in foodList:
            #get the manhattan distance to the food from pacman position
            manhattan = manhattanDistance(newPos, food)
            foodDistance.append(manhattan)
        if len(foodDistance):
            scoreAdd = FOOD_POINTS / min(foodDistance)
            score = score + scoreAdd
            return score
        
        return successorGameState.getScore()
    
def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minMaxFunction(gameState, depth, pacman):
            if pacman >= gameState.getNumAgents():
                depth += 1
                pacman = 0
                
            if depth==self.depth:
                return self.evaluationFunction(gameState)
            elif gameState.isWin():
                return self.evaluationFunction(gameState)
            elif gameState.isLose():
                return self.evaluationFunction(gameState)         
            elif (pacman == 0):
                #if the next agent is max, then return max function
                return maxFunction(gameState, depth, pacman)
            else:
                #if the next agent is min, then return min function
                return minFunction(gameState, depth, pacman)
        
        def minFunction(gameState, depth, pacman):
            POSITIVE_INFINITY = float("inf")
            range = [0, POSITIVE_INFINITY]
            successorState = gameState.getLegalActions(pacman)
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(pacman, next)
                successorsValue = minMaxFunction(getSuccessors, depth, pacman+1)
                #store the value in temporary
                if type(successorsValue) is list:
                    temporary = successorsValue[1]
                else:
                    temporary = successorsValue
                #check the range of the value, if it is less then range, change the
                # max value of range to temporary
                if temporary < range[1]:
                    range = [next, temporary]
            return range
        
        
        def maxFunction(gameState, depth, pacman):
            NEGATIVE_INFINITY = -float("inf")
            range = [0, NEGATIVE_INFINITY]
            successorState = gameState.getLegalActions(pacman)
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(pacman, next)
                successorsValue = minMaxFunction(getSuccessors, depth, pacman+1)
                #store the value in temporary
                if type(successorsValue) is list:
                    temporary = successorsValue[1]
                else:
                    temporary = successorsValue
                #check the range of the value, if it is greater then range, change the
                # min value of range to temporary
                if temporary > range[1]:
                    range = [next, temporary]                    
            return range
             
        rangeList = minMaxFunction(gameState, 0, 0)
        return rangeList[0]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        NEGATIVE_INFINITY = -float("inf")
        POSITIVE_INFINITY = float("inf")
        def minMaxHelper(gameState, depth, agent, alpha, beta):
            if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
            if depth==self.depth:
                return self.evaluationFunction(gameState)
            elif gameState.isWin():
                return self.evaluationFunction(gameState)
            elif gameState.isLose():
                return self.evaluationFunction(gameState)  
            elif (agent == 0):
                return maxFinder(gameState, depth, agent, alpha, beta)
            else:
                return minFinder(gameState, depth, agent, alpha, beta)


        def maxFinder(gameState, depth, agent, alpha, beta):
            range = [0, NEGATIVE_INFINITY]
            successorState = gameState.getLegalActions(agent)
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(agent, next)
                successorsValue = minMaxHelper(getSuccessors, depth, agent+1, alpha, beta)
                
                if type(successorsValue) is list:
                    temporary = successorsValue[1]
                else:
                    temporary = successorsValue
                    
                if temporary > range[1]:
                    range = [next, temporary]
                if temporary > beta:
                    return [next, temporary]
                alpha = max(alpha, temporary)
            return range
        
        
        def minFinder(gameState, depth, agent, alpha, beta):
            range = [0, POSITIVE_INFINITY]
            successorState = gameState.getLegalActions(agent)
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(agent, next)
                successorsValue = minMaxHelper(getSuccessors, depth, agent+1, alpha, beta)
                
                if type(successorsValue) is list:
                    temporary = successorsValue[1]
                else:
                    temporary = successorsValue
                    
                    
                if temporary < range[1]:
                    range = [next, temporary]
                if temporary < alpha:
                    return [next, temporary]
                beta = min(beta, temporary)
            return range
             
        rangeList = minMaxHelper(gameState, 0, 0, NEGATIVE_INFINITY, POSITIVE_INFINITY)
        return rangeList[0]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectiMaxFunction(gameState, depth, agent):
            if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
            if agent >= gameState.getNumAgents():
                agent = 0
                depth += 1
            if depth==self.depth:
                return self.evaluationFunction(gameState)
            elif gameState.isWin():
                return self.evaluationFunction(gameState)
            elif gameState.isLose():
                return self.evaluationFunction(gameState) 
            elif (agent == 0):
                return maxFunction(gameState, depth, agent)
            else:
                return expectiFunction(gameState, depth, agent)

        def expectiFunction(gameState, depth, agent):
            range = [0, 0]
            successorState = gameState.getLegalActions(agent)
            
            if not successorState:
                return self.evaluationFunction(gameState)
                
            weight = 1.0/len(successorState)    
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(agent, next)
                successorValue = expectiMaxFunction(getSuccessors, depth, agent+1)
                if type(successorValue) is list:
                    val = successorValue[1]
                else:
                    val = successorValue
                range[0] = next
                range[1] += val * weight
            return range
        
        def maxFunction(gameState, depth, agent):
            NEGATIVE_INFINITY = -float("inf")
            range = [0, NEGATIVE_INFINITY]
            successorState = gameState.getLegalActions(agent)
            
            if not successorState:
                return self.evaluationFunction(gameState)
                
            for next in successorState:
                getSuccessors = gameState.generateSuccessor(agent, next)
                successorValue = expectiMaxFunction(getSuccessors, depth, agent+1)
                if type(successorValue) is list:
                    testVal = successorValue[1]
                else:
                    testVal = successorValue
                if testVal > range[1]:
                    range = [next, testVal]                    
            return range
             
        rangeList = expectiMaxFunction(gameState, 0, 0)
        return rangeList[0]    
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"   
    foodCoord = currentGameState.getFood().asList() 
    distance = []  
    currentPos = list(currentGameState.getPacmanPosition()) 
    
 
    for food in foodCoord:
        manhattan = manhattanDistance(food, currentPos)
        manhattan = -1 * manhattan
        distance.append(manhattan)
    
    if not distance:
        distance.append(0)
    
    score = max(distance) + currentGameState.getScore() 
    return score

# Abbreviation
better = betterEvaluationFunction