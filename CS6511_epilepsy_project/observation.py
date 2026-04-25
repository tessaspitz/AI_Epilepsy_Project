import random

# observation model for noisy patient reporting
# this file handles what we actually see from a patient
# the true state may not be perfectly known in real life

# possible noise for reported seizure level, which means the report can be one level lower, exact, or one level higher
seizure_noise = [-1, 0, 1]

# possible noise for reported side effects (side effects can also be slightly underreported or overreported)
side_effect_noise = [-1, 0, 1]