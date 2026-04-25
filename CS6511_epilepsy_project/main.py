from state import *
from actions import allowed_actions
from transitions import transition_model, reward_function
from mdp import MDP
from value_iteration import value_iteration, extract_policy


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

    print("Done. Total states:", len(V))


if __name__ == "__main__":
    main()