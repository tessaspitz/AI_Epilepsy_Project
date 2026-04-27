from actions import allowed_actions


class MDP:
    def __init__(self, states, transition, reward, gamma=0.95):
        self.states = states
        self.transition = transition
        self.reward = reward
        self.gamma = gamma

def compute_q_value(mdp, V, state, action):
    total = 0
    transitions = mdp.transition(state, action)

    for prob, next_state in transitions:
        total = total + prob * (mdp.reward(state, action, next_state) + mdp.gamma * V[next_state])

    return total
    

def get_best_action(mdp, V, state):
    actions = allowed_actions(state)

    if len(actions) == 0:
        return None
    
    best_action = None
    best_value = -999999

    for action in actions:
        q_value = compute_q_value(mdp, V, state, action)

        if q_value > best_value:
            best_value = q_value
            best_action = action

    return best_action