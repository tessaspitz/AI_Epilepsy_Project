# prints the top states based on their value
def print_top_values(V, num_states=10):

    sorted_values = sorted(V.items(), key=lambda item: item[1], reverse=True) # sort states from highest value to lowest value

    print("\ntop state values")
    print("----------------")

    # print only the top few states
    for state, value in sorted_values[:num_states]:
        print(f"state = {state}, value = {round(value, 3)}")


# prints the lowest-value states
def print_bottom_values(V, num_states=10):

    sorted_values = sorted(V.items(), key=lambda item: item[1]) # sort states from lowest value to highest value

    print("\nbottom state values")
    print("-------------------")

    # print only the bottom few states
    for state, value in sorted_values[:num_states]:
        print(f"state = {state}, value = {round(value, 3)}")


# counts how often each action appears in the final policy
def print_policy_action_counts(policy):

    action_counts = {}

    # go through every state/action pair in the policy
    for state, action in policy.items():

        # if we have not seen the action yet, start it at 0
        if action not in action_counts:
            action_counts[action] = 0

        action_counts[action] += 1 # add one to the action count

    print("\npolicy action counts")
    print("--------------------")

    # print how often each action was chosen
    for action, count in action_counts.items():
        print(f"{action}: {count}")


# prints a cleaner summary of the simulation history
def print_simulation_summary(history, total_reward):

    print("\nsimulation summary")
    print("------------------")

    # handle case where simulation did not run any steps
    if len(history) == 0:
        print("no simulation steps were recorded")
        return

    average_reward = total_reward / len(history) # calculate average reward per step

    print(f"steps simulated: {len(history)}")
    print(f"total reward: {round(total_reward, 3)}")
    print(f"average reward per step: {round(average_reward, 3)}")
    print(f"start state: {history[0]['state']}")
    print(f"end state: {history[-1]['next_state']}")