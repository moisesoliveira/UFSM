import mdp, util
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """

  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """

    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
     
    "*** YOUR CODE HERE ***"
    self.iteration = 0
    for i in range(iterations):    
        self.new_values = util.Counter() # cria um dicionario com o valor padrao 0
        for state in self.mdp.getStates() :
	    next_best_action = self.getAction(state) # retorna a politica do estado
	    if next_best_action == None:
                continue
            self.new_values[state] = self.getQValue(state, next_best_action) # valor Q do par estado acao 
        self.values = self.new_values  # atribui os novos valores ao dicionario antigo
  

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """

    "*** YOUR CODE HERE ***"
    next_sp = self.mdp.getTransitionStatesAndProbs(state,action)
    value = 0
    for next_state, prob in next_sp:
            reward = self.mdp.getReward(state,action,next_state)
            value += prob * (reward + self.discount * self.values[next_state])
    return value

    util.raiseNotDefined()


  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"

    possible_actions = self.mdp.getPossibleActions(state) # acoes possiveis dado um estado
    best_value = -99999999 # seta o valor do melhor valor para um numero extremamente baixo
    best_action = None

    for action in possible_actions:
        value = self.getQValue(state,action)  # valor Q do par estado acao 
        if value > best_value : 	      # se valor calculado eh maior que o melhor valor 
            best_value = value                # melhor valor torna-se o valor calculado anteriormente
            best_action = action              # melhor acao passa a ser a calculada anteriormente
    return best_action

    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
