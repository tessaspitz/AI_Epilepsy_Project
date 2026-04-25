class MDP:
    def __init__(self, states, transition, reward, gamma=0.95):
        self.states = states
        self.transition = transition
        self.reward = reward
        self.gamma = gamma