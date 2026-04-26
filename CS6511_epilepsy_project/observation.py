import random

# observation model for noisy patient reporting
# this file handles what we actually see from a patient
# the true state may not be perfectly known in real life

# possible noise for reported seizure level, which means the report can be one level lower, exact, or one level higher
seizure_noise = [-1, 0, 1]

# possible noise for reported side effects (side effects can also be slightly underreported or overreported)
side_effect_noise = [-1, 0, 1]

# convert side effect labels into numbers, this makes it easier to move severity up or down
side_effect_to_num = {
    "none": 0,
    "mild": 1,
    "moderate": 2,
    "high": 3
}

# convert numbers back into labels to keep the observation in the same style as the state space
num_to_side_effect = {
    0: "none",
    1: "mild",
    2: "moderate",
    3: "high"
}

# generate a noisy observation from the true state, which simulates a patient report or clinical measurement
def observe(state):
    seizures, treatment, side_effect, duration = state

    # add noise to seizure level
    seizure_change = random.choice(seizure_noise)
    observed_seizures = seizures + seizure_change

    # keep seizure level inside the valid range
    observed_seizures = max(0, min(5, observed_seizures))

    # convert side effect burden to a number
    side_effect_num = side_effect_to_num[side_effect]

    # add noise to side effect burden
    side_effect_change = random.choice(side_effect_noise)
    observed_side_effect_num = side_effect_num + side_effect_change

    # keep side effect burden inside the valid range
    observed_side_effect_num = max(0, min(3, observed_side_effect_num))

    # convert back to the original side effect label
    observed_side_effect = num_to_side_effect[observed_side_effect_num]

    # observation only includes what we assume is imperfectly reported
    return (observed_seizures, observed_side_effect)

# estimate how likely an observation is given the true state which will be useful later for particle filtering/belief updates
def observation_likelihood(state, observation):
    seizures, treatment, side_effect, duration = state
    observed_seizures, observed_side_effect = observation

    probability = 1.0 # start with probability 1 and multiply each observation likelihood in
    
    seizure_difference = abs(seizures - observed_seizures) # compare the observed seizure level to the true seizure level

    # exact reports are most likely, nearby reports are still possible
    if seizure_difference == 0:
        probability *= 0.7
    elif seizure_difference == 1:
        probability *= 0.25
    else:
        probability *= 0.05

    # compare the observed side effect level to the true side effect level
    true_side_effect_num = side_effect_to_num[side_effect]
    observed_side_effect_num = side_effect_to_num[observed_side_effect]

    # same idea as seizures: exact is most likely, close is somewhat likely
    side_effect_difference = abs(true_side_effect_num - observed_side_effect_num)
    if side_effect_difference == 0:
        probability *= 0.7
    elif side_effect_difference == 1:
        probability *= 0.25
    else:
        probability *= 0.05

    return probability # return the final likelihood of this observation