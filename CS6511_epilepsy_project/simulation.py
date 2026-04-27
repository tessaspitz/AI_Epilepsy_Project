import random


# chooses an action for the current state, if we have a policy, follow it, otherwise just pick something random (temporary)
def choose_action(state, policy, actions):
    if policy is not None and state in policy:
        return policy[state]

    return random.choice(actions)


# figures out what the next state should be, supports both deterministic and probabilistic transitions
def get_next_state(state, action, transitions):

    possible_next_states = transitions[state][action] # grab all possible next states for this (state, action)

    # if it's just a single state (not a list), return it directly
    if not isinstance(possible_next_states, list):
        return possible_next_states

    # otherwise, assume it's a list of (state, probability)
    # will sample using cumulative probability
    rand_num = random.random()
    cumulative_prob = 0

    for next_state, prob in possible_next_states:
        cumulative_prob += prob

        # once we pass the random number, we pick that state
        if rand_num <= cumulative_prob:
            return next_state

    # fallback in case probabilities don't sum perfectly to 1
    return possible_next_states[-1][0]


# gets the reward for taking an action in a state
def get_reward(state, action, rewards):
    return rewards[state][action]


# runs the simulation for a given number of steps and tracks what happens at each step + total reward
def run_simulation(states, actions, transitions, rewards, policy=None, start_state=None, num_steps=10):

    # choose starting state (default=first state)
    if start_state is None:
        current_state = states[0]
    else:
        current_state = start_state

    total_reward = 0 # keeps track of cumulative reward
    history = [] # stores everything that happens

    # loop through each step in the simulation
    for step in range(num_steps):

        action = choose_action(current_state, policy, actions) # decide what action to take
        reward = get_reward(current_state, action, rewards) # get reward from current state + action
        next_state = get_next_state(current_state, action, transitions) # move to next state
        total_reward += reward # update total reward

        # store what happened this step (useful for debugging later)
        history.append({
            "step": step,
            "state": current_state,
            "action": action,
            "reward": reward,
            "next_state": next_state
        })

        current_state = next_state # update current state for next loop iteration

    return history, total_reward


# prints results in a clean way
def print_simulation_results(history, total_reward):

    print("simulation results")
    print("------------------")

    # go through each step and print what happened
    for item in history:
        print(
            f"step {item['step']}: "
            f"state = {item['state']}, "
            f"action = {item['action']}, "
            f"reward = {item['reward']}, "
            f"next state = {item['next_state']}"
        )

    print("------------------")
    print(f"total reward: {total_reward}")