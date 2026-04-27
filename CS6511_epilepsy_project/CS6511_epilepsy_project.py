"""
C6511 Project: Epilepsy Treatment Planning, A Sequential Decision Problem
Mohamad Koubeissi, Tessa Spitz, Aurora Stankow-Mercer

A state will be" (seizure_level, treatment_stage, side_effect_burden, time_in_stage)
"""

#-----------------------------Section 5.1.3 State Space Implementation-------------------------------

import random

seizure_levels = [0, 1, 2, 3, 4, 5]

seizure_labels = {
    0: "seizure-free",
    1: "low seizure frequency (1 in 3 months)",
    2: "low-moderate seizure frequency (2 in 3 months)",
    3: "moderate-high seizure frequency (3-4 in 3 months)",
    4: "high seizure frequency (4-9 in 3 months)",
    5: "severe seizure frequency (>= 10 in 3 months)",
}

treatment_stages = [
    "low_dose_monotherapy",
    "high_dose_monotherapy",
    "dual_therapy",
    "triple_therapy",
    "polypharmacy",
    "surgical_evaluation",
]

side_effect_burdens = ["none", "mild", "moderate", "high"]

time_in_stage = list(range(11))   # number of visits (every 3 months) in this stage

# Generate full raw state space
state_space = []

for seizures in seizure_levels:
    for treatment in treatment_stages:
        for side_effect in side_effect_burdens:
            for duration in time_in_stage:
                state_space.append((seizures, treatment, side_effect, duration))

# boolean function to exclude invalid states
def is_valid_state(state):
    seizures, treatment, side_effect, duration = state

    # Rule 1:
    # low-dose monotherapy should not continue too long if seizures remain >= 2
    if treatment == "low_dose_monotherapy" and seizures >= 2 and duration > 2:
        return False

    # Rule 2:
    # surgical evaluation should only happen for more severe epilepsy
    if treatment == "surgical_evaluation" and seizures < 3:
        return False

    # Rule 3:
    # triple therapy usually implies the patient has already spent some time escalating
    if treatment == "triple_therapy" and duration < 4:
        return False

    return True

# Filter to valid states
states = []
for state in state_space:
    if is_valid_state(state):
        states.append(state)

# generate dictionaries assiginig a number ID for each state
def build_state_mappings(states):
    state_to_id = {}
    id_to_state = {}

    for i, state in enumerate(states):
        state_to_id[state] = i
        id_to_state[i] = state

    return state_to_id, id_to_state

state_to_id, id_to_state = build_state_mappings(states)

# print states nicely
def describe_state(state):
    assert is_valid_state(state), "Invalid state."

    seizures, treatment, side_effect, duration = state

    return (
        f"Seizure level: {seizure_labels[seizures]}\n"
        f"Treatment stage: {treatment}\n"
        f"Side effect burden: {side_effect}\n"
        f"Number of visits in this stage: {duration}"
    )

################################ TEST PRINT ########################################

example_state1 = (1, "high_dose_monotherapy", "mild", 10)

test_print_1 = False
if test_print_1:
    print("=" * 77)
    print(describe_state(example_state1))
    print("=" * 77)
    print("Total raw states:", len(state_space))
    print("Total valid states:", len(states))
    print("Example state ID:", state_to_id[example_state1])
    print("Reverse lookup:", id_to_state[state_to_id[example_state1]])
    print("=" * 77)

####################################################################################

# how the state space is distributed across treatment stages
states_by_treatment = {}
for treatment in treatment_stages:
    states_for_each = []
    states_by_treatment[treatment] = states_for_each
    for state in states:
        if state[1] == treatment:
            states_for_each.append(state)

################################ TEST PRINT ########################################

test_print_2a = False
if test_print_2a:
    print("\nStates by treatment stage:")
    for treatment in treatment_stages:
        print(f"{treatment}: {len(states_by_treatment[treatment])}")

####################################################################################

# define favorable states
def is_goal_state(state):
    seizures, treatment, side_effect, duration = state
    if seizures == 0 and (side_effect == "none" or side_effect == "mild"):
        return True
    return False

# understand whether constraints disproportionately remove certain types of states.
states_by_seizure_level = {}
for seizure in seizure_levels:
    states_for_each = []
    states_by_seizure_level[seizure] = states_for_each
    for state in states:
        if state[0] == seizure:
            states_for_each.append(state)

################################ TEST PRINT ########################################

test_print_2b = False
if test_print_2b:
    for i in states_by_seizure_level:
        print(f"seizure level {i}: {seizure_labels[i]}, number of states {len(states_by_seizure_level[i])}")

####################################################################################

actions = [
    "continue_current",
    "increase_dose",
    "switch_medication",
    "add_medication",
    "refer_for_surgery",
]

def allowed_actions(state):
    assert is_valid_state(state), "Invalid state."

    seizures, treatment, side_effect, duration = state

    # goal states: if seizure-free with none/mild side effects, continue current treatment
    if is_goal_state(state):
        return ["continue_current"]

    # default actions depend on treatment stage
    if treatment == "low_dose_monotherapy":
        allowed = {
            "continue_current",
            "increase_dose",
            "switch_medication",
            "add_medication",
        }

    elif treatment == "high_dose_monotherapy":
        allowed = {
            "continue_current",
            "switch_medication",
            "add_medication",
        }

    elif treatment == "dual_therapy":
        allowed = {
            "continue_current",
            "switch_medication",
            "add_medication",
            "refer_for_surgery",
        }

    elif treatment == "triple_therapy":
        allowed = {
            "continue_current",
            "switch_medication",
            "add_medication",
            "refer_for_surgery",
        }

    elif treatment == "polypharmacy":
        allowed = {
            "continue_current",
            "switch_medication",
            "refer_for_surgery",
        }

    elif treatment == "surgical_evaluation":
        # don't change medications for surgical patients
        allowed = {
            "continue_current",
        }

    else:
        allowed = set()

    # don't increase dose when there are significant side effects
    if side_effect == "moderate" or side_effect == "high":
        allowed.discard("increase_dose")

    # if seizure burden is still substantial, do not allow passive continuation alone
    # but only remove continue_current if other reasonable actions exist
    if seizures >= 2 and treatment != "surgical_evaluation":
        if len(allowed) > 1 and "continue_current" in allowed:
            allowed.discard("continue_current")

    # surgery should only be available for sufficiently high seizure burden
    if seizures < 3:
        allowed.discard("refer_for_surgery")

    # return actions in the original display order
    ordered_allowed = [action for action in actions if action in allowed]
    return ordered_allowed

################################ TEST PRINT ########################################

test_print_3 = False
if test_print_3:
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
            print("=" * 77)
            print(f"State: {s}")
            print(describe_state(s))
            print("Allowed actions:", allowed_actions(s))
        else:
            print("=" * 77)
            print(f"Invalid test state: {s}")

####################################################################################

# explain why a state is invalid
def invalid_reason(state):
    seizures, treatment, side_effect, duration = state

    if treatment == "low_dose_monotherapy" and seizures >= 2 and duration > 2:
        return "low-dose monotherapy persisted too long despite poor seizure control"

    if treatment == "surgical_evaluation" and seizures < 3:
        return "surgical evaluation is not allowed for seizure levels below 3"

    if treatment == "triple_therapy" and duration < 4:
        return "triple therapy requires at least 4 visits in stage"

    return "valid"

################################ TEST PRINT ########################################

test_print_4 = False
if test_print_4:
    candidate_states = [
        (2, "low_dose_monotherapy", "mild", 3),
        (1, "surgical_evaluation", "none", 0),
        (4, "triple_therapy", "moderate", 2),
        (4, "dual_therapy", "mild", 2),
    ]

    for s in candidate_states:
        print(s, "->", invalid_reason(s))

####################################################################################

# Below, I'm explicitly handling boundary conditions
def improve_seizures(seizures):
    if seizures == 0:
        return 0
    return seizures - 1

def worsen_seizures(seizures):
    if seizures == 5:
        return 5
    return seizures + 1

def improve_side_effect(side_effect):
    if side_effect == "high":
        return "moderate"
    elif side_effect == "moderate":
        return "mild"
    elif side_effect == "mild":
        return "none"
    else:
        return "none"

def worsen_side_effect(side_effect):
    if side_effect == "none":
        return "mild"
    elif side_effect == "mild":
        return "moderate"
    elif side_effect == "moderate":
        return "high"
    else:
        return "high"
    
def advance_treatment_stage(treatment):
    if treatment == "low_dose_monotherapy":
        return "high_dose_monotherapy"
    elif treatment == "high_dose_monotherapy":
        return "dual_therapy"
    elif treatment == "dual_therapy":
        return "triple_therapy"
    elif treatment == "triple_therapy":
        return "polypharmacy"
    else:
        return treatment

def make_next_state(seizures, treatment, side_effect, duration):
    next_state = (seizures, treatment, side_effect, duration)

    if is_valid_state(next_state):
        return next_state

    return None

# now we're ready to build transition model:
def transition_model(state, action):
    assert is_valid_state(state), "Invalid current state."
    assert action in allowed_actions(state), "Invalid action for this state."

    seizures, treatment, side_effect, duration = state

    transitions = []

    if action == "continue_current":
        candidates = [
            (0.15, improve_seizures(seizures), treatment, side_effect, duration + 1),
            (0.60, seizures, treatment, side_effect, duration + 1),
            (0.15, worsen_seizures(seizures), treatment, side_effect, duration + 1),
            (0.10, seizures, treatment, worsen_side_effect(side_effect), duration + 1),
        ]

    elif action == "increase_dose":
        candidates = [
            (0.40, improve_seizures(seizures), treatment, side_effect, duration + 1),
            (0.20, improve_seizures(seizures), treatment, worsen_side_effect(side_effect), duration + 1),
            (0.15, seizures, treatment, worsen_side_effect(side_effect), duration + 1),
            (0.15, seizures, treatment, side_effect, duration + 1),
            (0.10, worsen_seizures(seizures), treatment, side_effect, duration + 1),
        ]

    elif action == "switch_medication":
        candidates = [
            (0.30, improve_seizures(seizures), treatment, improve_side_effect(side_effect), 0),
            (0.25, seizures, treatment, improve_side_effect(side_effect), 0),
            (0.20, seizures, treatment, side_effect, 0),
            (0.15, worsen_seizures(seizures), treatment, side_effect, 0),
            (0.10, seizures, treatment, worsen_side_effect(side_effect), 0),
        ]

    elif action == "add_medication":
        new_treatment = advance_treatment_stage(treatment)

        candidates = [
            (0.45, improve_seizures(seizures), new_treatment, side_effect, 0),
            (0.20, improve_seizures(seizures), new_treatment, worsen_side_effect(side_effect), 0),
            (0.15, seizures, new_treatment, worsen_side_effect(side_effect), 0),
            (0.10, seizures, new_treatment, side_effect, 0),
            (0.10, worsen_seizures(seizures), new_treatment, side_effect, 0),
        ]

    elif action == "refer_for_surgery":
        candidates = [
            (0.50, improve_seizures(improve_seizures(seizures)), "surgical_evaluation", side_effect, 0),
            (0.20, improve_seizures(seizures), "surgical_evaluation", side_effect, 0),
            (0.15, seizures, "surgical_evaluation", side_effect, 0),
            (0.10, seizures, "surgical_evaluation", worsen_side_effect(side_effect), 0),
            (0.05, worsen_seizures(seizures), "surgical_evaluation", side_effect, 0),
        ]

    else:
        raise ValueError("Unknown action.")

    for prob, next_seizures, next_treatment, next_side_effect, next_duration in candidates:

        # enforcing duration boundaries 
        if next_duration > max(time_in_stage):
            next_duration = max(time_in_stage)

        next_state = make_next_state(
            next_seizures,
            next_treatment,
            next_side_effect,
            next_duration
        )

        if next_state is not None:
            transitions.append((prob, next_state))

    if len(transitions) == 0:
        return [(1.0, state)]

    total_prob = sum(prob for prob, next_state in transitions)

    normalized_transitions = []
    for prob, next_state in transitions:
        normalized_transitions.append((prob / total_prob, next_state))

    return normalized_transitions

################################ TEST PRINT ########################################

example_state2 = (4, "high_dose_monotherapy", "moderate", 5)

test_print_5 = False
if test_print_5:
    print("=" * 77)
    print(transition_model(example_state2, "switch_medication"))
    print("=" * 77)

####################################################################################

# Now R(s, a, s'):
def reward_function(state, action, next_state):
    seizures, treatment, side_effect, duration = state
    next_seizures, next_treatment, next_side_effect, next_duration = next_state

    reward = 0

    # seizure outcome reward
    if next_seizures == 0:
        reward += 100
    elif next_seizures < seizures:
        reward += 30
    elif next_seizures == seizures:
        reward += 0
    else:
        reward -= 50

    # side effect penalty
    side_effect_penalties = {
        "none": 0,
        "mild": -5,
        "moderate": -20,
        "high": -40,
    }

    reward += side_effect_penalties[next_side_effect]

    # treatment burden penalty
    treatment_penalties = {
        "low_dose_monotherapy": 0,
        "high_dose_monotherapy": -5,
        "dual_therapy": -10,
        "triple_therapy": -20,
        "polypharmacy": -30,
        "surgical_evaluation": -15,
    }

    reward += treatment_penalties[next_treatment]

    # reward appropriate referral for refractory epilepsy
    if action == "refer_for_surgery" and seizures >= 3:
        reward += 20

    # penalty for doing nothing when seizures are substantial
    if action == "continue_current" and seizures >= 3:
        reward -= 25

    return reward

################################ TEST PRINT ########################################

example_state3 = (4, "high_dose_monotherapy", "moderate", 5)
example_state4 = (1, "dual_therapy", "mild", 6)

test_print_6 = False
if test_print_6:
    print("=" * 77)
    print(reward_function(example_state3, "switch_medication", example_state4))
    print("=" * 77)

####################################################################################
