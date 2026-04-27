from state import *
from actions import allowed_actions
from transitions import transition_model, reward_function
from mdp import MDP
from value_iteration import value_iteration, extract_policy
from policy_iteration import policy_iteration
from simulation import run_simulation, run_particle_simulation, print_simulation_results
from results import (
    print_top_values,
    print_bottom_values,
    print_policy_action_counts,
    print_simulation_summary
)


def main():

    mdp = MDP(states, transition_model, reward_function)

    print("\n" + "="*77)
    print("TEST 1: Example state description")
    print(describe_state((2, "high_dose_monotherapy", "mild", 10)))
    print("="*77)

    print("\n" + "="*77)
    print("TEST 2: States by treatment stage")
    for t in treatment_stages:
        print(t, ":", len(states_by_treatment[t]))
    print("="*77)

    print("\n" + "="*77)
    print("TEST 3: Allowed actions")
    s = (4, "dual_therapy", "mild", 3)
    print("State:", s)
    print("Allowed:", allowed_actions(s))
    print("="*77)

    print("\n" + "="*77)
    print("TEST 4: Invalid reason")
    s = (2, "low_dose_monotherapy", "mild", 3)
    print(s, "->", invalid_reason(s))
    print("="*77)

    print("\n" + "="*77)
    print("TEST 5: Transition example")
    s = (4, "high_dose_monotherapy", "moderate", 5)
    print(transition_model(s, "switch_medication"))
    print("="*77)

    print("\n" + "="*77)
    print("TEST 6: Reward example")
    s1 = (4, "high_dose_monotherapy", "moderate", 5)
    s2 = (2, "high_dose_monotherapy", "moderate", 6)
    print(reward_function(s1, "switch_medication", s2))
    print("="*77)

    print("\nRunning value iteration...\n")
    V = value_iteration(mdp)
    policy = extract_policy(mdp, V)

    print("Value iteration done. Total states:", len(V))

    print_top_values(V)
    print_bottom_values(V)
    print_policy_action_counts(policy)

    print("\nRunning regular simulation...\n")

    start_state = (4, "high_dose_monotherapy", "moderate", 5)

    history, total_reward = run_simulation(
        mdp=mdp,
        policy=policy,
        start_state=start_state,
        num_steps=10
    )

    print_simulation_results(history, total_reward)
    print_simulation_summary(history, total_reward)

    print("\nRunning particle simulation...\n")

    particle_history = run_particle_simulation(
        mdp=mdp,
        policy=policy,
        start_state=start_state,
        num_steps=10,
        num_particles=1000
    )

    print("particle simulation results")
    print("---------------------------")

    for item in particle_history:
        print(item)

    print("\nRunning policy iteration...\n")

    pi_policy, pi_values = policy_iteration(mdp)

    print("Policy iteration done.")
    print_policy_action_counts(pi_policy)


if __name__ == "__main__":
    main()