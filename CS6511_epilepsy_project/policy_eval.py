from mdp import compute_q_value
from actions import allowed_actions
from state import describe_state
from value_iteration import value_iteration, extract_policy
from state import states


def policy_evaluation(policy, states, gamma=0.9, theta=1e-4, max_iterations=1000):
    U = {}

    for state in states:
        U[state] = 0

    for iteration in range(max_iterations):
        delta = 0

        for state in states:
            old_value = U[state]
            action = policy[state]

            if action is None:
                continue

            U[state] = compute_q_value(state, action, U, gamma)

            delta = max(delta, abs(old_value - U[state]))

        if delta < theta:
            break

    return U

def policy_improvement(policy, U, states, gamma=0.9):
    policy_stable = True
    new_policy = policy.copy()

    for state in states:
        old_action = policy[state]
        actions_for_state = allowed_actions(state)

        if not actions_for_state:
            continue

        best_action = None
        best_value = float("-inf")

        for action in actions_for_state:
            q = compute_q_value(state, action, U, gamma)

            if q > best_value:
                best_value = q
                best_action = action

        new_policy[state] = best_action

        if best_action != old_action:
            policy_stable = False

    return new_policy, policy_stable

def policy_iteration(states, gamma=0.9, theta=1e-4, max_policy_iterations=100):
    policy = {}

    for state in states:
        actions_for_state = allowed_actions(state)

        if actions_for_state:
            policy[state] = actions_for_state[0]
        else:
            policy[state] = None

    for iteration in range(max_policy_iterations):
        U = policy_evaluation(policy, states, gamma, theta)
        policy, stable = policy_improvement(policy, U, states, gamma)

        if stable:
            print("Policy iteration converged after", iteration + 1, "iterations.")
            break
    else:
        print("Policy iteration reached max_policy_iterations without full convergence.")

    return policy, U

############################### TEST PRINT ########################################

example_state = (1, "low_dose_monotherapy", "high", 3)

test_print = False

if test_print:
    policy_pi, U_pi = policy_iteration(states, gamma=0.9, theta=1e-4, max_policy_iterations=100)
    print(describe_state(example_state6))
    print("Policy iteration action:", policy_pi[example_state6])
    print("Utility:", U_pi[example_state6])

####################################################################################

def compare_policies(policy_1, policy_2, states):
    differences = []

    for state in states:
        if policy_1[state] != policy_2[state]:
            differences.append(state)

    return differences

# Controlled run block: run MDP solvers once, then use their outputs in tests/simulations.
# Keep this False while editing/debugging. Set to True when you want to run the full project.

run_mdp = False

if run_mdp:
    U_vi = value_iteration(states, gamma=0.9, theta=1e-4, max_iterations=1000)
    policy_vi = extract_policy(states, U_vi, gamma=0.9)

    policy_pi, U_pi = policy_iteration(states, gamma=0.9, theta=1e-4, max_policy_iterations=100)

    differences = compare_policies(policy_vi, policy_pi, states)

    print("Value iteration complete.")
    print("Policy iteration complete.")
    print("Number of policy differences:", len(differences))

####################################################################################
