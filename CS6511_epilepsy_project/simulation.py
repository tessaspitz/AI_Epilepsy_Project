import random
from observation import observe
from particle_filter import initialize_particles, update_particles, summarize_belief
from actions import allowed_actions

# sample the next state using the mdp transition model
def sample_next_state(mdp, state, action):
    transitions = mdp.transition(state, action)

    probabilities = [prob for prob, next_state in transitions]
    next_states = [next_state for prob, next_state in transitions]

    next_state = random.choices(next_states, weights=probabilities, k=1)[0]

    return next_state


# runs the simulation for a given number of steps and tracks what happens at each step + total reward
def run_simulation(mdp, policy, start_state, num_steps=10):
    current_state = start_state

    total_reward = 0 # keeps track of cumulative reward
    history = [] # stores everything that happens

    # loop through each step in the simulation
    for step in range(num_steps):

        action = policy[current_state] # decide what action to take from the policy
        next_state = sample_next_state(mdp, current_state, action) # move to next state
        reward = mdp.reward(current_state, action, next_state) # get reward from current state + action + next state
        observation = observe(next_state) # create a noisy observation of what happened

        total_reward += reward # update total reward

        # store what happened this step (useful for debugging later)
        history.append({
            "step": step,
            "state": current_state,
            "action": action,
            "reward": reward,
            "next_state": next_state,
            "observation": observation
        })

        current_state = next_state # update current state for next loop iteration

    return history, total_reward


# runs a simulation while tracking belief with particles
def run_particle_simulation(mdp, policy, start_state, num_steps=10, num_particles=100):
    true_state = start_state
    particles = initialize_particles(mdp.states, num_particles)

    history = [] # stores everything that happens

    # loop through each step in the simulation
    for step in range(num_steps):

        belief = summarize_belief(particles) # summarize what the particles currently believe

        estimated_state = max(belief, key=belief.get) # use the most likely state as the estimate
        action = policy.get(estimated_state)

        action = policy.get(estimated_state)
        valid_actions = allowed_actions(true_state)

        if action not in valid_actions:
            if len(valid_actions) > 0:
                action = valid_actions[0]
            else:
                action = None
        if action is None:
            break

        #action = policy[estimated_state] # choose action based on estimated state

        next_true_state = sample_next_state(mdp, true_state, action) # actual hidden patient state moves forward
        observation = observe(next_true_state) # noisy observation of the true next state

        particles = update_particles(particles, action, observation, mdp) # update belief using action + observation

        # store what happened this step (useful for debugging later)
        history.append({
            "step": step,
            "true_state": true_state,
            "estimated_state": estimated_state,
            "action": action,
            "observation": observation,
            "next_true_state": next_true_state
        })

        true_state = next_true_state # update true state for next loop iteration

    return history


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
            f"next state = {item['next_state']}, "
            f"observation = {item['observation']}"
        )

    print("------------------")
    print(f"total reward: {total_reward}")