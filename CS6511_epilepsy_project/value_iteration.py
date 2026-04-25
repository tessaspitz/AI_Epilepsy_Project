def value_iteration(mdp, iterations=100):
    V = {}
    for state in mdp.states:
        V[state] = 0.0
    for i in range(iterations):
        new_V = {}
        for state in mdp.states:
            possible_actions = allowed_actions(state)
            if len(possible_actions) == 0:
                new_V[state] = 0.0
                continue
            best_value = -99999999
            for action in possible_actions:
                q_value = compute_q_value(mdp, V, state, action)
                if q_value > best_value:
                    best_value = q_value
            new_V[state] = best_value
        V = new_V
    return V


def extract_policy(mdp, V):
    policy = {}
    for state in mdp.states:
        best_action = get_best_action(mdp, V, state)
        policy[state] = best_action
    return policy