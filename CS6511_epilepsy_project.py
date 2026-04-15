"""
C6511 Project: Epilepsy Treatment Planning, A Sequential Decision Problem
Mohamad Koubeissi, Tessa Spitz, Aurora Stankow-Mercer

A state will be" (seizure_level, treatment_stage, side_effect_burden, time_in_stage)
"""

'''
---------------------------------------------------Section 5.1.3 State Space Implementation---------------------------------------------------------------------------------------------------------------
'''


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

time_in_stage = list(range(25))   # number of visits (every 3 months) in this stage

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
    if treatment == "surgical_evaluation" and seizures == 0:
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

# Example 
example_state = (2, "high_dose_monotherapy", "mild", 10)

################################ TEST PRINT ########################################
test_print_1 = False
if test_print_1:
    print("\n")
    print("=" * 77)
    print(describe_state(example_state))
    print("=" * 77)
    print("Total raw states:", len(state_space))
    print("Total valid states:", len(states))
    print("Example state ID:", state_to_id[example_state])
    print("Reverse lookup:", id_to_state[state_to_id[example_state]])
    print("=" * 77)
    print("\n")
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
test_print_2 = False
if test_print_2:
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



'''
--------------------------------------------------------Section 5.1.2 State Space Description---------------------------------------------------------------------------------------------------
'''

'''
(1) Our project models epilepsy treatment plans as a sequential decision problem, where each 
patients' condition evolves over time based on treatment decisions and outcomes. 

A state represents the patient's current clinical situation and is defined by our four components:
seizure level, treatment stage, side effect burden, and time spent in the current treamtent stage. 

The seizure level captures how frequently the patient experiences seizures, ranging from seizure-free 
to severe epilepsy. The treatment stage reflects the current level of medical intervention, from low-dose
monotherapy to surgical evaluation. Side effect burden represents the severity of treatment side effects,
and time in stage tracks how long the patient has remained in their current treatment plan. 

At each step, a doctor can choose an action, such as continuing the current treatment, increasing
dosage, switching medications, adding medications, or referring the patient to surgery. These decisions 
impact how the patient transitions to the next state. 

The system is stochastic, meaning that the outcomes are uncertain: the same treatment deicisons may 
lead to different sizure outcomes or side effects. The goal is to guide the patient (and doctor) towards 
favorable states where seizures are minimized (or eliminated entirely) while side effects remain low. 
'''

'''
* Note: I'm using this symbol: ε to denote "belongs in" since I don't know how to actually get the real symbol on VS Code. 

(2) A state may b e defined as a tuple: s = (z, t, e,d) where
    x ε {0, 1, 2, 3, 4, 5}: seizure level
    t ε T: treatment stage where T = {low_dose_monotherapy, high_dose_monotherapy, dual_therapy, 
    triple_therapy, polypharmacy, surgical_evaluation}
    e ε {none, mild, moderate, high}: side effect burden
    d ε {i | 0 <= i < = 24}: time (number of visits) in current stage 

The valid state space S is a subset of X * T * E * D for this problem is restricted by certain constraints:
    1. Low-dose monotherapy cannot persist with high seizure levels beyind a short duration
    2. Surgical evaluation is only allowed for sufficiently sever seizure levels
    3. Advanced therapies reaquire sufficient prior treatment duration

Action Space: 
    The set of possible actions is A = {continue_current, increase_dose, switch_medication, 
    add_medication, refer_for_surgery}. 
    The available actions depend on the current state: A(s) is a subset of A. 
    (E.g. if side effects are high, the doctor may not increase the dosage. 
    Or if seizure level is severe, continuing current treatment may not be allowed).

Transition function: 
    The system changes according to a probabilistic function P(s' | s, a) where 
        - s is the current state
        - a ε A(s) is the chosen action
        - s' is the next state
    Transitions capture the following:
        - Changes in seizure level (improved, worsened, the same)
        - Changes in side effect burden
        - Movement between treatment stages
        - Increament of time in stage
    We will use the following probabilities:
        - P(seizures decrease without side effects) = 0.4
        - P(seizures decrease and side effects worsen) = 0.2
        - P(no change in seizure frequency and side effects worsen) = 0.15
        - P(no change in seizure frequency and no side effects) = 0.15
        - P(seizures worsen ) = 0.1

    Reward/Utility Function: The goal is to maximize patient quality of life, which is a balance between 
    seizure control and medication side effects. We plan to use: 
        - +100 for seizure freedom
        - +20 for seizure reduction
        - -30 for severe side effects
        - -100 severe seizure exacerbation

Goal States:
    We will define favorable outcomes (goal states) as:
        - x = 0 AND
        - e ε {none, mild}
    These represent seizure free patients with minimal side effects. 

''' 