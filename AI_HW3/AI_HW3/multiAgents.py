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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


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
    Your minimax agent (Part 1)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        Explanation :
        define a backtracking function to do the minimax.
        this function will track down along the depth and the agents.
        if the current state is a terminal state, it returns the score;

        if this agent is the pacman, it choose the action with the highest score among the scores that the first ghost evaluates
        (using recursion),and return the score and action to backtrack to the agents with upper level;
        
        if this agent is the ghost, it will return the action and the lowest score among the scores that the next agent evaluates.
        The backtracking process is done in this function. getAction() simply calls the action of the top node and return it.
        """
        # back tracking to do minimax scoring
        def minimax(self, gameState, depth, agentIndex):
            # terminal states
            if gameState.isWin() or gameState.isLose() or depth >= self.depth:
                return [self.evaluationFunction(gameState),None] # current score, next move
            
            # pacman moves
            if agentIndex == 0:
                best_value = -1e9
                next_move = None
                # each branches
                for action in gameState.getLegalActions(0):
                    next_value = minimax(self, gameState.getNextState(0,action), depth, 1)
                    # get max value
                    if next_value[0] > best_value :
                        best_value = next_value[0]
                        next_move = action
                return [best_value,next_move]
            # ghost response
            else:
                best_value = 1e9
                next_response = None 
                for response in gameState.getLegalActions(agentIndex):
                    next_value = []
                    # last ghost
                    if agentIndex == gameState.getNumAgents()-1:
                        next_value = minimax(self, gameState.getNextState(agentIndex,response), depth+1, 0)
                    # other ghost
                    else:
                        next_value = minimax(self, gameState.getNextState(agentIndex,response), depth, agentIndex+1)
                    # get min value
                    if next_value[0] < best_value:
                        best_value = next_value[0]
                        next_response = response
                return [best_value, next_response]
        # result of minimax : the first action
        result = minimax(self,gameState,0,0)
        return result[1]
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """  
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        Explanation:
        define a backtracking function to do the minimax with alpha-beta pruning.
        this function will track down along the depth and the agents.
        if the current state is a terminal state, it returns the score;
        
        if this agent is the pacman, it choose the action with the highest score among the scores that the first ghost evaluates
        (using recursion), then updates the alpha value. If the alpha is greater than the beta, return the current value,
        meaning that this branch is being pruned; else return the score, action and updated alpha
        to backtrack to the agents with upper level;

        if this agent is the ghost, it will choose the action and the lowest score among the scores that the next agent evaluates,
        then updates the beta value. If the alpha is greater than the beta, return the current value,
        meaning that this branch is being pruned; else returns the lowest score and the updated beta.
        The backtracking process is done in this function. getAction() simply calls the action of the top node and return it.
        """
            # optimized version of minimax with introduction of alpha (value of maximizer) and beta (value of minimizer)
        def alpha_beta(self, gameState, depth, agentIndex, alpha ,beta):
            new_alpha = alpha
            new_beta = beta
            # terminal states
            if gameState.isWin() or gameState.isLose() or depth >= self.depth:
                return [self.evaluationFunction(gameState),None] # current score, next move
            
            # pacman moves (updates alpha, check on beta)
            if agentIndex == 0:
                best_value = -1e9
                next_move = None
                # each branches
                for action in gameState.getLegalActions(0):
                    next_value = alpha_beta(self, gameState.getNextState(0,action), depth, 1, new_alpha, new_beta)
                    # get max value
                    if next_value[0] > best_value :
                        best_value = next_value[0]
                        next_move = action
                    # update alpha
                    new_alpha = max(new_alpha,best_value)
                    # check for beta, if alpha > beta then minimizer will ignore this branch
                    if new_alpha > new_beta :
                        return [best_value,next_move]     

                return [best_value,next_move]

            # ghost response
            else:
                best_value = 1e9
                next_response = None 
                for response in gameState.getLegalActions(agentIndex):
                    next_value = [] # for if branches
                    # last ghost
                    if agentIndex == gameState.getNumAgents()-1:
                        next_value = alpha_beta(self, gameState.getNextState(agentIndex,response), depth+1, 0, 
                                new_alpha, new_beta)
                    # other ghost
                    else:
                        next_value = alpha_beta(self, gameState.getNextState(agentIndex,response), 
                                depth, agentIndex+1, new_alpha, new_beta)
                    # get min value
                    if next_value[0] < best_value:
                        best_value = next_value[0]
                        next_response = response
                    # updates beta
                    new_beta = min(new_beta,best_value)
                    # check for alpha, if beta < alpha then maximizer will ignore this branch
                    if new_beta < new_alpha:
                        return [best_value,next_response]

            return [best_value, next_response]
        result = alpha_beta(self,gameState,0,0,-1e9,1e9)
        return result[1]
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        Explanation:
        define a backtracking function to do the expectimax.
        this function will track down along the depth and the agents.
        if the current state is a terminal state, it returns the score;
        
        if this agent is the pacman, it choose the action with the highest score among the scores that the first ghost evaluates
        (using recursion),and return the score and action to backtrack to the agents with upper level;

        if this agent is the ghost, it evaluates the average score of its legal actions and return it
        to the upper level agents with recursion, without making a legal move.
        """
        # assume the adversary plays uniformly at random
        def expectimax(self, gameState, depth, agentIndex):
            # terminal states
            if gameState.isWin() or gameState.isLose() or depth >= self.depth:
                return [self.evaluationFunction(gameState),None] # current score, next move
            
            # pacman moves
            if agentIndex == 0:
                best_value = -1e9
                next_move = None
                # each branches
                for action in gameState.getLegalActions(0):
                    next_value = expectimax(self, gameState.getNextState(0,action), depth, 1)
                    # get max value
                    if next_value[0] > best_value :
                        best_value = next_value[0]
                        next_move = action
                return [best_value,next_move]
            # ghost response ,now they are chance nodes
            else:
                chance_value = 0
                legal_actions = gameState.getLegalActions(agentIndex)
                for response in legal_actions:
                    next_value = []
                    # last ghost
                    if agentIndex == gameState.getNumAgents()-1:
                        next_value = expectimax(self, gameState.getNextState(agentIndex,response), depth+1, 0)
                    # other ghost
                    else:
                        next_value = expectimax(self, gameState.getNextState(agentIndex,response), depth, agentIndex+1)
                    # get expectation value instead
                    chance_value += next_value[0]
                chance_value /= len(legal_actions)
                return [chance_value, None]
        result = expectimax(self, gameState, 0, 0)
        return result[1]
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    Explanation:
    This evaluation function furtherly consider the food distance, ghost distance and the capsule
    first, gain the position of the pacman, foods and the ghosts using the current game state. 
    calculate the distance to the nearest food using manhattan distance, since this function is faster than maze-distancing.
    If there's any food nearby, evaluate the score for food distance : the higher the point, agent is the closer to the food. 
    
    Next, evaluate the score with the ghosts.
    If the ghost is not scared, the score receive an exponential penalty for getting closer to the ghost, for a distance < 4
    Else if the ghost is scared, meaning pac-man ate a capsule, then receive a bonus for eatting scared ghost.

    Finally, sum up the evaluation above and the original evaluation score for the scoring of winning and losing states. 
    then return this final score.
    """
    pacman_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    closet_food_dist = 1e9
    food_eval = 0
    # find closet food
    for food in food_list:
        closet_food_dist = min(manhattanDistance(pacman_pos,food), closet_food_dist)
    # evaluation on food
    if closet_food_dist == 1e9:
        food_eval = 0
    else:
        food_eval = -0.25 * closet_food_dist
    # evaluation on ghost and capsule
    ghost_states = currentGameState.getGhostStates()
    ghost_eval = 0
    capsule_eval = 0
    for ghost_state in ghost_states:
        ghost_pos = ghost_state.getPosition()
        # not scared by capsule
        if ghost_state.scaredTimer <= 0:
            if manhattanDistance(pacman_pos,ghost_pos) <= 4:
                ghost_eval -= (4-manhattanDistance(pacman_pos,ghost_pos))**3
        # got capusle
        else:
            capsule_eval += 15
    # sum of evaluation
    return food_eval + ghost_eval + capsule_eval + scoreEvaluationFunction(currentGameState)
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
