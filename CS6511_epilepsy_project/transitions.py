from state import is_valid_state, time_in_stage
from actions import allowed_actions

# now building transition model
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