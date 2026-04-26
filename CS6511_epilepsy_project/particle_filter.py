import random

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