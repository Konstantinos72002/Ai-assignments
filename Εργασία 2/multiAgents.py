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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        newFood = successorGameState.getFood().asList()
        
        # Ignore states who ghosts are near to pacman
        for ghost in successorGameState.getGhostPositions():
            if manhattanDistance(ghost,newPos) < 2 :
                return float("-inf")
        
        # Find the nearest food
        nearest_food = float("inf")
        for food in newFood:
            nearest_food = min(nearest_food,manhattanDistance(food,newPos))
    
        # Evaluate by the score and the distance from the nearest food
        return successorGameState.getScore() + 1.0/nearest_food
    
def scoreEvaluationFunction(currentGameState: GameState):
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
    # Max agend
    def Max(self, gameState: GameState, depth):
        
        # Evaluate cases if case is win or lose or depth <= 0
        if gameState.isWin() or gameState.isLose() or depth <= 0:
            return self.evaluationFunction(gameState), Directions.STOP
    
        n = float("-inf")
        action_list = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            action_list.append(self.Min(gameState.generateSuccessor(0,action),depth-1)[0])
            n = max(n,self.Min(gameState.generateSuccessor(0,action),depth-1)[0])
        for i in range(len(action_list)):
            if action_list[i] == n:
                best_move = actions[i]
        
        return n , best_move
    
    # Min agends
    def Min(self, gameState: GameState, depth):
        if gameState.isWin() or gameState.isLose() or depth <= 0:
            return self.evaluationFunction(gameState), Directions.STOP
        num_of_agents = gameState.getNumAgents()
        n = float("inf")
        action_list = []
        actions = gameState.getLegalActions(abs((depth % num_of_agents) - num_of_agents))
        if (depth - 1) % num_of_agents == 0:
            for action in actions:
                action_list.append(self.Max(gameState.generateSuccessor(abs(depth % num_of_agents - num_of_agents),action),depth-1)[0])
                n = min(n,self.Max(gameState.generateSuccessor(abs(depth % num_of_agents - num_of_agents),action),depth-1)[0])
            for i in range(len(action_list)):
                if action_list[i] == n:
                    best_move = actions[i]
                    return n,best_move
        else:
            for action in actions:
                action_list.append(self.Min(gameState.generateSuccessor(abs((depth%num_of_agents)-num_of_agents),action),depth-1)[0])
                n = min(n,self.Min(gameState.generateSuccessor(abs((depth%num_of_agents)-num_of_agents),action),depth-1)[0])
            for i in range(len(action_list)):
                if action_list[i] == n:
                    best_move = actions[i]
                    return n , best_move
    
        

    def getAction(self, gameState: GameState):
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
        real_depth = self.depth*gameState.getNumAgents()
        return self.Max(gameState,real_depth)[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def Max(self, gameState: GameState, depth,a,b):
        if gameState.isWin() or gameState.isLose() or depth <= 0:
            return self.evaluationFunction(gameState), Directions.STOP
    
        n = float("-inf")
        action_list = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            action_list.append(self.Min(gameState.generateSuccessor(0,action),depth-1,a,b)[0])
            n = max(n,self.Min(gameState.generateSuccessor(0,action),depth-1,a,b)[0])
            if n > b:
                break
            a = max(a,n)
        for i in range(len(action_list)):
            if action_list[i] == n:
                best_move = actions[i]
        
        return n , best_move
    
    def Min(self, gameState: GameState, depth,a,b):
        if gameState.isWin() or gameState.isLose() or depth <= 0:
            return self.evaluationFunction(gameState), Directions.STOP
        num_of_agents = gameState.getNumAgents()
        n = float("inf")
        action_list = []
        actions = gameState.getLegalActions(abs((depth % num_of_agents) - num_of_agents))
        if (depth - 1) % num_of_agents == 0:
            for action in actions:
                action_list.append(self.Max(gameState.generateSuccessor(abs(depth % num_of_agents - num_of_agents),action),depth-1,a,b)[0])
                n = min(n,self.Max(gameState.generateSuccessor(abs(depth % num_of_agents - num_of_agents),action),depth-1,a,b)[0])
                if n < a:
                    break
                b = min(b,n)
            for i in range(len(action_list)):
                if action_list[i] == n:
                    best_move = actions[i]
                    return n,best_move
        else:
            for action in actions:
                action_list.append(self.Min(gameState.generateSuccessor(abs((depth%num_of_agents)-num_of_agents),action),depth-1,a,b)[0])
                n = min(n,self.Min(gameState.generateSuccessor(abs((depth%num_of_agents)-num_of_agents),action),depth-1,a,b)[0])
                if n < a:
                    break
                b = min(b,n)
            for i in range(len(action_list)):
                if action_list[i] == n:
                    best_move = actions[i]
                    return n , best_move
                
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        a = float("-inf")
        b = float("inf")
        real_depth = self.depth*gameState.getNumAgents()
        return self.Max(gameState,real_depth,a,b)[1]
        
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def Max(self, gameState: GameState, depth):
        if gameState.isWin() or gameState.isLose() or depth <= 0:
            return self.evaluationFunction(gameState), Directions.STOP
    
        n = float("-inf")
        action_list = []
        actions = gameState.getLegalActions(0)
        for action in actions:
            action_list.append(self.Evaluate(gameState.generateSuccessor(0,action),depth-1))
            if self.Evaluate(gameState.generateSuccessor(0,action),depth-1) >= n:
                n = self.Evaluate(gameState.generateSuccessor(0,action),depth-1)
                best_move = action
        return n , best_move
    
    def Evaluate(self, gameState: GameState, depth):
        if gameState.isWin() or gameState.isLose() or depth < 0:
            return self.evaluationFunction(gameState)
        num_of_agents = gameState.getNumAgents()
        actions = gameState.getLegalActions(abs((depth % num_of_agents) - num_of_agents))
        if (depth - 1) % num_of_agents == 0:
            p = 1/len(actions)
            s = 0
            for action in actions:
                s += p*self.Max(gameState.generateSuccessor(abs((depth%num_of_agents) - num_of_agents),action),depth-1)[0]
            return s
        else:
            p = 1/len(actions)
            s = 0
            for action in actions:
                s += p*self.Evaluate(gameState.generateSuccessor(abs((depth%num_of_agents)-num_of_agents),action),depth-1)
            return s
        
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        real_depth = self.depth*gameState.getNumAgents()
        return self.Max(gameState,real_depth)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    # Win and Lose cases
    if currentGameState.isWin():
        return 99999999999999999999
    if currentGameState.isLose():
        return -99999999999999999999
    
    pac_man_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
   
    e_1 = 0
    if len(food_list) != 0:
        e_1 = 1/len(food_list)
    
    # distance from min food
    min_dist = float("inf")
    for food in food_list:
        min_dist = min(min_dist,manhattanDistance(food,pac_man_pos))
    e2 = 1/min_dist
    
    # score of the state
    e3 = currentGameState.getScore()
    
    
    
    return e_1 + 10*e2 + e3
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
