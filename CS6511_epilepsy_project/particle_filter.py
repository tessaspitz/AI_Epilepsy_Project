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


# update particles after receiving a new observation, the part that corrects the belief using what we observed
def update_particles(particles, observation):
    weighted_particles = weight_particles(particles, observation)
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