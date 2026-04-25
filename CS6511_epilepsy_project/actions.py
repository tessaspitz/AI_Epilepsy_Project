from state import is_valid_state

actions = [
    "continue_current",
    "increase_dose",
    "switch_medication",
    "add_medication",
    "refer_for_surgery",
]

# define favorable states
def is_goal_state(state):
    seizures, treatment, side_effect, duration = state
    if seizures == 0 and (side_effect == "none" or side_effect == "mild"):
        return True
    return False

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