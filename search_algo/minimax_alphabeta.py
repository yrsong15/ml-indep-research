import random
from sys import maxint

minimaxNodes = 0
alphabetaNodes = 0 

class GamePlayer(object):
    '''Represents the logic for an individual player in the game'''

    def __init__(self, player_id, game):
        '''"player_id" indicates which player is represented (int)
        "game" is a game object with a get_successors function'''
        self.player_id = player_id
        self.game = game
        return

    def evaluate(self, state):
        '''Evaluates a given state for the specified agent
        "state" is a game state object'''
        pass

    def minimax_move(self, state):
        '''Returns a string action representing a move for the agent to make'''
        pass

    def alpha_beta_move(self, state):
        '''Same as minimax_move with alpha-beta pruning'''
        pass


class BasicPlayer(GamePlayer):
    '''A basic agent which takes random (valid) actions'''

    def __init__(self, player_id, game):
        GamePlayer.__init__(self, player_id, game)

    def evaluate(self, state):
        '''This agent doesn't evaluate states, so just return 0'''
        return 0

    def minimax_move(self, state):
        '''Don't perform any game-tree expansions, just pick a random move
            that's available in the list of successors'''
        assert state.player == self.player_id
        successors, actions = self.game.get_successors(state)
        # Take a random successor's action
        return random.choice(actions)

    def alpha_beta_move(self, state):
        '''Just calls minimax_move'''
        return self.minimax_move(state)


def minimax_dfs(game, state, depth, horizon, eval_fn):
    global minimaxNodes
    minimaxNodes += 1
    successors, actions = game.get_successors(state)
    value = -maxint
    action = ''
    for i in range(len(successors)):
        newState = successors[i]
        temp = minValue(game, newState, depth+1, horizon, eval_fn)
        if temp > value:
            value = temp
            action = actions[i]
    return value, action

def maxValue(game, state, depth, horizon, eval_fn):
    global minimaxNodes
    minimaxNodes += 1
    if depth == horizon: 
        return eval_fn(state)
    successors, actions = game.get_successors(state)
    ret = -maxint 
    compare = -1
    for i in range(len(successors)):
        newState = successors[i]
        compare = minValue(game, newState, depth+1, horizon, eval_fn)
        if compare > ret:
            ret = compare
    return ret

def minValue(game, state, depth, horizon, eval_fn):
    global minimaxNodes
    minimaxNodes += 1
    if depth == horizon: 
        return eval_fn(state)
    successors, actions = game.get_successors(state)
    ret = maxint
    compare = -1
    for i in range(len(successors)):
        newState = successors[i]
        compare = maxValue(game, newState, depth+1, horizon, eval_fn)
        if compare < ret:
            ret = compare
    return ret

def alphabeta_dfs(game, state, depth, horizon, eval_fn):
    global alphabetaNodes
    alphabetaNodes += 1
    successors, actions = game.get_successors(state)
    compare = -maxint
    action = ''
    for i in range(len(successors)):
        newState = successors[i]
        temp = alphaBetaMinValue(game, newState, depth+1, horizon, eval_fn, -maxint, maxint)
        if temp > compare:
            compare = temp
            action = actions[i]
    return action


def alphaBetaMaxValue(game, state, depth, horizon, eval_fn, alpha, beta):
    global alphabetaNodes
    alphabetaNodes += 1
    if depth == horizon:
        return eval_fn(state)
    successors, actions = game.get_successors(state)
    temp = -maxint
    for i in range(len(successors)):
        newState = successors[i]
        temp = max(temp, alphaBetaMinValue(game, newState, depth+1, horizon, eval_fn, alpha, beta))
        if temp >= beta: return temp
        alpha = max(alpha, temp)
    return temp

def alphaBetaMinValue(game, state, depth, horizon, eval_fn, alpha, beta):
    global alphabetaNodes
    alphabetaNodes += 1
    if depth == horizon:
        return eval_fn(state)
    successors, actions = game.get_successors(state)
    temp = maxint
    for i in range(len(successors)):
        newState = successors[i]
        temp = min(temp, alphaBetaMaxValue(game, newState, depth+1, horizon, eval_fn, alpha, beta))
        if temp <=alpha: return temp
        beta = min(beta, temp)
    return temp

def distanceFromCookies(xCor, yCor, distancePenalty, state):
    retVal = 0
    for row in range(len(state.grid)):
        for col in range(len(state.grid[row])):
            if state.grid[row][col] == 'c':
                retVal += (abs(xCor-row) + abs(yCor-col)) * distancePenalty
    # print "Penalty: ",retVal
    return retVal

def numberOfCookies(state):
    retVal = 0
    for row in range(len(state.grid)):
        for col in range(len(state.grid[row])):
            if state.grid[row][col] == 'c':
                retVal += 1
    return retVal

class StudentPlayer(GamePlayer):
    def __init__(self, player_id, game):
        GamePlayer.__init__(self, player_id, game)

    def evaluate(self, state):
        if state.player == 0: opponentID = 1
        else: opponentID = 0; 
        currentCookies = 100
        lastCookie = 0
        if numberOfCookies(state)==0: lastCookie = 100000 #this is to prevent the last cookie not being eaten
        distancePenalty = 1
        myScore = state.cookiecounts[state.player] * currentCookies
        oppScore = state.cookiecounts[opponentID] * currentCookies
        myXCor, myYCor, oppXCor, oppYCor = -1, -1, -1, -1
        for row in range(len(state.grid)):
            for col in range(len(state.grid[row])):
                if state.grid[row][col] == str(state.player):
                    myXCor = row
                    myYCor = col
                if state.grid[row][col] == str(opponentID):
                    oppXCor = row
                    oppYCor = col
        assert (myXCor>=0 and myYCor >=0 and oppXCor >=0 and oppYCor >=0)
        myScore -= distanceFromCookies(myXCor, myYCor, distancePenalty, state)
        oppScore -= distanceFromCookies(oppXCor, oppYCor, distancePenalty, state)
        myScore += lastCookie
        return myScore-oppScore

    def minimax_move(self, state):
        assert state.player == self.player_id
        # Experiment with the value of horizon
        horizon = 6
        val, action = minimax_dfs(self.game, state, 0, horizon, self.evaluate)
        print "# of Minimax Nodes: ", minimaxNodes
        return action

    def alpha_beta_move(self, state):
        assert state.player == self.player_id
        horizon = 6
        action = alphabeta_dfs(self.game, state, 0, horizon, self.evaluate)
        print "# of Alphabeta Nodes: ", alphabetaNodes
        return action
