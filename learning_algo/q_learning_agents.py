from learning_agents import ReinforcementAgent
import random
from sys import maxint

class QLearningAgent(ReinforcementAgent):

    def __init__(self, **args):
        """Initialize Q-values"""
        super(QLearningAgent, self).__init__(**args)
        self.qValues = dict()
        self.terminal_state = 'TERMINAL_STATE'
        self.counter = 0
        self.initGlobalGrid()
        # self.pretty_print_grid(globalGrid)

    def get_q_value(self, state, action):
        """
        Returns Q(state,action)
        Should return 0.0 if we never seen
        a state or (state,action) tuple
        """
        if (state,action) not in self.qValues:
            self.qValues[(state,action)] = 0.0

        return self.qValues[(state,action)]

    def get_value(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.  Note that if
        there are no legal actions, which is the case at the
        terminal state, you should return a value of 0.0.
        """
        # if state==self.terminal_state: return 0.0
        if len(self.get_legal_actions(state))==0: 
            return 0.0
        legalActions = self.get_legal_actions(state)
        temp = -maxint
        for nextAction in legalActions:
            if self.get_q_value(state, nextAction) > temp:
                temp = self.get_q_value(state, nextAction)
        return temp

    def get_policy(self, state):
        """
        Compute the best action to take in a state.  Note that if there
        are no legal actions, which is the case at the terminal state,
        you should return None.
        """
        if state==self.terminal_state: 
            return None
        if len(self.get_legal_actions(state))==0: 
            return None
        legalActions = self.get_legal_actions(state)
        temp = -maxint
        bestAction = None
        for nextAction in legalActions:
            if self.get_q_value(state, nextAction) > temp:
                temp = self.get_q_value(state, nextAction)
                bestAction = nextAction
        return bestAction

    def get_action(self, state):
        """
        Compute the action to take in the current state.  With
        probability self.epsilon, we should take a random action and
        take the best policy action otherwise.  Note that if there are
        no legal actions, which is the case at the terminal state, you
        should choose None as the action.
        """
        legalActions = self.get_legal_actions(state)
        if state==self.terminal_state or len(self.get_legal_actions(state))==0: 
            return None
        if random.random() < self.epsilon:
            return random.choice(legalActions)
        else:
            return self.get_policy(state)

    def update(self, state, action, nextState, reward):
        """
        The parent class calls this to observe a
        state = action => nextState and reward transition.
        """
        self.qValues[(state,action)] = self.get_q_value(state, action) + \
                self.alpha*(reward + self.discount*(self.get_q_value(nextState, self.get_action(nextState)))-self.get_q_value(state, action))

    def setGlobalGrid(self, xcor, ycor, val):
        global globalGrid
        globalGrid[xcor][ycor] = val

    def initGlobalGrid(self):
        global globalGrid
        globalGrid = [[0 for x in range(5)] for y in range(14)]

    def pretty_print_grid(self, grid):
        print "-------------"
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                temp = (i, j)
                print self.get_value(temp),
            print ""
    def print_grid(self):
        for key,value in self.qValues.iteritems():
            print key[0]
            print key[1]
            print value
            print "-------------"
