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

    ###### STATE SPACE TESTS
    print("\n" + "="*80)
    print("STATE SPACE TESTS")
    print("="*80)

    example_state = (2, "high_dose_monotherapy", "mild", 10)
    print("\nTEST 1: Example state space tests")
    print(describe_state(example_state))
    print("Total raw states: ", len(state_space))
    print("Total valid states:", len(states))
    print("State ID:", state_to_id[example_state])
    print("Reverse lookup:", id_to_state[state_to_id[example_state]])

    print("\nStates by Treatment Stage:")
    for t in treatment_stages:
        print(t, ":", len(states_by_treatment[t]))

    print("\nStates by Seizure Level:")
    for s in states_by_seizure_level:
        print(f"seizure level {s}: {len(states_by_seizure_level[s])}")

    ##### ACTION TESTS
    print("\n" + "="*80)
    print("ACTION TESTS")
    print("="*80)

    s = (4, "dual_therapy", "mild", 3)
    print("\nSingle State:", s)
    print("Allowed actions:", allowed_actions(s))

    print("\nMultiple State Action Checks:")
    test_states = [
        (0, "low_dose_monotherapy", "none", 1),
        (1, "low_dose_monotherapy", "mild", 2),
        (2, "high_dose_monotherapy", "moderate", 1),
        (4, "dual_therapy", "mild", 3),
        (5, "triple_therapy", "high", 6),
        (4, "surgical_evaluation", "moderate", 1),
    ]

    for s in test_states:
        if is_valid_state(s):
            print("\nState:", s)
            print("Allowed actions:", allowed_actions(s))
        else:
            print("Invalid state:", s)

    #### INVALID STATES TESTS
    print("\n" + "="*80)
    print("INVALID STATE TESTS")
    print("="*80)

    candidate_states = [
        (2, "low_dose_monotherapy", "mild", 3),
        (1, "surgical_evaluation", "none", 0),
        (4, "triple_therapy", "moderate", 2),
        (4, "dual_therapy", "mild", 2),
    ]

    for s in candidate_states:
        print(s, "->", invalid_reason(s))

    ####### TRANSITION TESTS
    print("\n" + "="*80)
    print("TRANSITION TEST")
    print("="*80)

    s = (4, "high_dose_monotherapy", "moderate", 5)
    print("Transitions:", transition_model(s, "switch_medication"))


    #######REWARD TESTS
    print("\n" + "="*80)
    print("REWARD TEST")
    print("="*80)

    s1 = (4, "high_dose_monotherapy", "moderate", 5)
    s2 = (2, "high_dose_monotherapy", "moderate", 6)
    print("Reward:", reward_function(s1, "switch_medication", s2))

    ##### VALUE ITERATION TESTS
    print("\n" + "="*80)
    print("VALUE ITERATION")
    print("="*80)

    V = value_iteration(mdp)
    policy = extract_policy(mdp, V)

    print("Value iteration done. Total states:", len(V))
    print_top_values(V)
    print_bottom_values(V)
    print_policy_action_counts(policy)


    ##### SIMULATION

    print("\n" + "="*80)
    print("SIMULATION")
    print("="*80)

    start_state = (4, "high_dose_monotherapy", "moderate", 5)

    history, total_reward = run_simulation(
        mdp=mdp,
        policy=policy,
        start_state=start_state,
        num_steps=10
    )

    print_simulation_results(history, total_reward)
    print_simulation_summary(history, total_reward)


    ###### PARTICLE FILTER SIM
    print("\n" + "="*80)
    print("PARTICLE FILTER SIMULATION")
    print("="*80)

    particle_history = run_particle_simulation(
        mdp=mdp,
        policy=policy,
        start_state=start_state,
        num_steps=10,
        num_particles=1000
    )

    for item in particle_history:
        print(item)

    ###### POLICY ITERATION
    print("\n" + "="*80)
    print("POLICY ITERATION")
    print("="*80)

    pi_policy, pi_values = policy_iteration(mdp)

    print("Policy iteration done.")
    print_policy_action_counts(pi_policy)

    print("\n" + "="*80)
    print("POLICY ITERATION CHECK (SINGLE STATE)")
    print("="*80)

    example_state = (1, "low_dose_monotherapy", "high", 3)
    print("State:", example_state)
    print("Best action:", pi_policy.get(example_state))
    print("Utility:", pi_values.get(example_state))


if __name__ == "__main__":
    main()