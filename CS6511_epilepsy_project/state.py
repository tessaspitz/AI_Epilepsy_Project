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

# understand whether constraints disproportionately remove certain types of states.
states_by_seizure_level = {}
for seizure in seizure_levels:
    states_for_each = []
    states_by_seizure_level[seizure] = states_for_each
    for state in states:
        if state[0] == seizure:
            states_for_each.append(state)

# how the state space is distributed across treatment stages
states_by_treatment = {}
for treatment in treatment_stages:
    states_for_each = []
    states_by_treatment[treatment] = states_for_each
    for state in states:
        if state[1] == treatment:
            states_for_each.append(state)