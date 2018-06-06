from learning_agents import ValueEstimationAgent
from sys import maxint


class ValueIterationAgent(ValueEstimationAgent):
    """
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Take an mdp on construction, 
          run the indicated number of iterations
          and then act according to the resulting policy.
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = dict((s, 0.0) for s in mdp.get_states())

        self.initGlobalGrid()

        print "Current Discount Factor: ", self.discount
        print "--------Beginning State----------"
        self.pretty_print_grid(globalGrid)
        print "--------"
        for i in range(0, self.iterations):
            global globalGrid
            for state,value in self.values.iteritems():
                bestAction = self.get_policy(state)
                temp = self.mdp.get_reward(state)
                if bestAction is None: continue
                for nextState, prob in mdp.get_transition_states_and_probabilities(state, bestAction):
                    temp += self.discount*prob*self.get_value(nextState)
                self.values[state] = temp
                self.setGlobalGrid(state[0], state[1], temp)
            if i==0 or i==1 or i==99:
                print "--------Iteration Number: " , i , " --------"
                self.pretty_print_grid(globalGrid)
                print "--------"
            
    def get_value(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def get_q_value(self, state, action):
        """
          The q-value of the state action pair
          (after the indicated number of value iteration
          passes).  Note that value iteration does not
          necessarily create this quantity and you may have
          to derive it on the fly.
        """
        #*** YOUR CODE HERE ***
        raise NotImplementedError()

    def get_policy(self, state):
        """
          The policy is the best action in the given state
          according to the values computed by value iteration.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        val = -maxint
        bestAction = None
        if self.mdp.is_terminal(state): return None
        for action in self.mdp.get_possible_actions(state):
            temp = self.mdp.get_reward(state)
            for nextState, prob in self.mdp.get_transition_states_and_probabilities(state, action):
                temp += self.discount*prob*self.get_value(nextState)
            if temp > val: 
                val = temp
                bestAction = action
        return bestAction

    def get_action(self, state):
        """"Returns the policy at the state (no exploration)."""
        return self.get_policy(state)

    def setGlobalGrid(self, xcor, ycor, val):
        global globalGrid
        globalGrid[xcor][ycor] = val

    def initGlobalGrid(self):
        global globalGrid
        globalGrid = [[0 for x in range(5)] for y in range(14)]

    def pretty_print_grid(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                print grid[i][j],
            print ""
