import random
from observation import observation_likelihood

# particle filter for tracking possible hidden patient states
# the idea is that we keep a bunch of possible true states then
# update them as we get noisy observations from the patient


# initialize particles by randomly choosing states from the state space, so each particle represents one possible true patient state
def initialize_particles(states, num_particles=100):
    particles = []

    # randomly sample possible states
    for i in range(num_particles):
        particle = random.choice(states)
        particles.append(particle)

    return particles

# move one particle forward using the transition model, this is the prediction step before using the observation
def predict_particle(particle, action, mdp):
    transitions = mdp.transition(particle, action)

    probabilities = [prob for prob, next_state in transitions]
    next_states = [next_state for prob, next_state in transitions]

    predicted_particle = random.choices(next_states, weights=probabilities, k=1)[0]

    return predicted_particle


# move all particles forward after an action is taken, this approximates how the hidden patient state evolves
def predict_particles(particles, action, mdp):
    predicted_particles = []

    # predict each particle one at a time
    for particle in particles:
        predicted_particle = predict_particle(particle, action, mdp)
        predicted_particles.append(predicted_particle)

    return predicted_particles


# assign a weight to each particle based on the observation particles that better match the observation should matter more
def weight_particles(particles, observation):
    weighted_particles = []

    # go through each possible hidden state
    for particle in particles:
        weight = observation_likelihood(particle, observation)
        weighted_particles.append((particle, weight))

    return weighted_particles


# resample particles based on their weights (higher weight particles are more likely to survive)
def resample_particles(weighted_particles):
    particles = [particle for particle, weight in weighted_particles]
    weights = [weight for particle, weight in weighted_particles]

    # if all weights are zero, just resample uniformly, this prevents the filter from crashing
    if sum(weights) == 0:
        return random.choices(particles, k=len(particles))

    # weighted random sampling makes likely states appear more often
    new_particles = random.choices(particles, weights=weights, k=len(particles))

    return new_particles


# update particles after taking an action and receiving a new observation, this includes prediction and correction
def update_particles(particles, action, observation, mdp):
    predicted_particles = predict_particles(particles, action, mdp)
    weighted_particles = weight_particles(predicted_particles, observation)
    new_particles = resample_particles(weighted_particles)

    return new_particles

# summarize the belief state from the particles, this helps to see what the filter thinks is most likely
def summarize_belief(particles):
    counts = {}

    # count how many times each state appears
    for particle in particles:
        if particle not in counts:
            counts[particle] = 0
        counts[particle] += 1

    # convert counts into probabilities
    belief = {}
    for state in counts:
        belief[state] = counts[state] / len(particles)

    return belief