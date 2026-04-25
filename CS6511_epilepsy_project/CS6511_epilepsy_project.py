"""
C6511 Project: Epilepsy Treatment Planning, A Sequential Decision Problem
Mohamad Koubeissi, Tessa Spitz, Aurora Stankow-Mercer

A state will be" (seizure_level, treatment_stage, side_effect_burden, time_in_stage)
"""

'''
---------------------------------------------------Section 5.1.3 State Space Implementation---------------------------------------------------------------------------------------------------------------
'''



# Example 
example_state = (2, "high_dose_monotherapy", "mild", 10)

################################ TEST PRINT ########################################
test_print_1 = False
if test_print_1:
    print("\n")
    print("=" * 77)
    print(describe_state(example_state))
    print("=" * 77)
    print("Total raw states:", len(state_space))
    print("Total valid states:", len(states))
    print("Example state ID:", state_to_id[example_state])
    print("Reverse lookup:", id_to_state[state_to_id[example_state]])
    print("=" * 77)
    print("\n")
####################################################################################


################################ TEST PRINT ########################################
test_print_2a = False
if test_print_2a:
    print("\nStates by treatment stage:")
    for treatment in treatment_stages:
        print(f"{treatment}: {len(states_by_treatment[treatment])}")
####################################################################################


################################ TEST PRINT ########################################
test_print_2 = False
if test_print_2:
    for i in states_by_seizure_level:
        print(f"seizure level {i}: {seizure_labels[i]}, number of states {len(states_by_seizure_level[i])}")
####################################################################################


################################ TEST PRINT ########################################
test_print_3 = False
if test_print_3:
    test_states = [
        (0, "low_dose_monotherapy", "none", 1),
        (1, "low_dose_monotherapy", "mild", 2),
        (2, "high_dose_monotherapy", "moderate", 1),
        (4, "dual_therapy", "mild", 3),
        (5, "triple_therapy", "high", 6),
        (4, "surgical_evaluation", "moderate", 1),
    ]

    for s in test_states:
        if is_valid_state(s):
            print("=" * 77)
            print(describe_state(s))
            print("Allowed actions:", allowed_actions(s))
        else:
            print("=" * 77)
            print(f"Invalid test state: {s}")
####################################################################################


################################ TEST PRINT ########################################
test_print_4 = False
if test_print_4:
    candidate_states = [
        (2, "low_dose_monotherapy", "mild", 3),
        (1, "surgical_evaluation", "none", 0),
        (4, "triple_therapy", "moderate", 2),
        (4, "dual_therapy", "mild", 2),
    ]

    for s in candidate_states:
        print(s, "->", invalid_reason(s))
####################################################################################



'''
--------------------------------------------------------Section 5.1.2 State Space Description---------------------------------------------------------------------------------------------------
'''

'''
(1) Our project models epilepsy treatment plans as a sequential decision problem, where each 
patients' condition evolves over time based on treatment decisions and outcomes. 

A state represents the patient's current clinical situation and is defined by our four components:
seizure level, treatment stage, side effect burden, and time spent in the current treamtent stage. 

The seizure level captures how frequently the patient experiences seizures, ranging from seizure-free 
to severe epilepsy. The treatment stage reflects the current level of medical intervention, from low-dose
monotherapy to surgical evaluation. Side effect burden represents the severity of treatment side effects,
and time in stage tracks how long the patient has remained in their current treatment plan. 

At each step, a doctor can choose an action, such as continuing the current treatment, increasing
dosage, switching medications, adding medications, or referring the patient to surgery. These decisions 
impact how the patient transitions to the next state. 

The system is stochastic, meaning that the outcomes are uncertain: the same treatment deicisons may 
lead to different sizure outcomes or side effects. The goal is to guide the patient (and doctor) towards 
favorable states where seizures are minimized (or eliminated entirely) while side effects remain low. 
'''

'''
* Note: I'm using this symbol: ε to denote "belongs in" since I don't know how to actually get the real symbol on VS Code. 

(2) A state may b e defined as a tuple: s = (z, t, e,d) where
    x ε {0, 1, 2, 3, 4, 5}: seizure level
    t ε T: treatment stage where T = {low_dose_monotherapy, high_dose_monotherapy, dual_therapy, 
    triple_therapy, polypharmacy, surgical_evaluation}
    e ε {none, mild, moderate, high}: side effect burden
    d ε {i | 0 <= i < = 24}: time (number of visits) in current stage 

The valid state space S is a subset of X * T * E * D for this problem is restricted by certain constraints:
    1. Low-dose monotherapy cannot persist with high seizure levels beyind a short duration
    2. Surgical evaluation is only allowed for sufficiently sever seizure levels
    3. Advanced therapies reaquire sufficient prior treatment duration

Action Space: 
    The set of possible actions is A = {continue_current, increase_dose, switch_medication, 
    add_medication, refer_for_surgery}. 
    The available actions depend on the current state: A(s) is a subset of A. 
    (E.g. if side effects are high, the doctor may not increase the dosage. 
    Or if seizure level is severe, continuing current treatment may not be allowed).

Transition function: 
    The system changes according to a probabilistic function P(s' | s, a) where 
        - s is the current state
        - a ε A(s) is the chosen action
        - s' is the next state
    Transitions capture the following:
        - Changes in seizure level (improved, worsened, the same)
        - Changes in side effect burden
        - Movement between treatment stages
        - Increament of time in stage
    We will use the following probabilities:
        - P(seizures decrease without side effects) = 0.4
        - P(seizures decrease and side effects worsen) = 0.2
        - P(no change in seizure frequency and side effects worsen) = 0.15
        - P(no change in seizure frequency and no side effects) = 0.15
        - P(seizures worsen ) = 0.1

    Reward/Utility Function: The goal is to maximize patient quality of life, which is a balance between 
    seizure control and medication side effects. We plan to use: 
        - +100 for seizure freedom
        - +20 for seizure reduction
        - -30 for severe side effects
        - -100 severe seizure exacerbation

Goal States:
    We will define favorable outcomes (goal states) as:
        - x = 0 AND
        - e ε {none, mild}
    These represent seizure free patients with minimal side effects. 

''' 