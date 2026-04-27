from actions import allowed_actions
from mdp import compute_q_value, get_best_action

# policy iteration gives another way to solve the MDP
# instead of directly updating values like value iteration, it improves a policy over time


# create an initial policy by choosing the first allowed action for each state
def initialize_policy(mdp):
    policy = {}

    # go through every state in the model
    for state in mdp.states:
        actions = allowed_actions(state)

        # if there are no actions, store None
        if len(actions) == 0:
            policy[state] = None
        else:
            policy[state] = actions[0]

    return policy


# evaluate the current policy by repeatedly updating utilities, this estimates how good each state is under the current policy
def policy_evaluation(mdp, policy, theta=1e-6):
    V = {}

    # start all utilities at zero
    for state in mdp.states:
        V[state] = 0.0

    while True:
        delta = 0

        # update every state based on the action chosen by the current policy
        for state in mdp.states:
            old_value = V[state]
            action = policy[state]

            # if there is no action, keep value at zero
            if action is None:
                V[state] = 0.0
            else:
                V[state] = compute_q_value(mdp, V, state, action)

            # track how much values are changing
            difference = abs(old_value - V[state])
            if difference > delta:
                delta = difference

        # stop once utilities are barely changing
        if delta < theta:
            break

    return V


# improve the policy by choosing the best action according to the current utilities
def policy_improvement(mdp, V, policy):
    policy_stable = True
    new_policy = {}

    # go through every state and see if a better action exists
    for state in mdp.states:
        old_action = policy[state]
        best_action = get_best_action(mdp, V, state)

        new_policy[state] = best_action

        # if the best action changed, the policy is not stable yet
        if best_action != old_action:
            policy_stable = False

    return new_policy, policy_stable


# full policy iteration, alternates between evaluating the policy and improving it
def policy_iteration(mdp, theta=1e-6, max_iterations=100):
    policy = initialize_policy(mdp)

    for i in range(max_iterations):
        V = policy_evaluation(mdp, policy, theta)
        policy, policy_stable = policy_improvement(mdp, V, policy)

        # if policy did not change,done
        if policy_stable:
            break

    return policy, V