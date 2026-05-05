# AI_Epilepsy_Project

Problem Statement:
Epilepsy treatment is a very complex, long-term process in which doctors must continuously adjust treatment plans based on uncertain patient outcomes. Patients may respond differently to medications, experience varying levels of side effects, and they may progress unpredictably over time. 

This project models epilepsy treatment planning as a stochastic sequential decision problem, where a doctor must repeatedly choose actions (like adding or switching medications, or recommending surgery) while accounting for the uncertainty that may come in the patient response to that decision. The goal of this project is to determine treatment strategies that minimize seizure frequency and severity level as well as minimizing side effects. 

Related solutions to a similar problem:
Sequential decision making in healthcare is commonly modeled using Markov Decision Processes (MDPs) for fully observable problems, Partially Observable MDPS (POMDPs) when patient states are uncertain, and reinforcement learning approaches for optimizing long-term treatment strategies. 

These approaches have been used in chronic disease treatment/management, including diabetes and cancer treatment planning[^1]. Our project follows a similar structure but focuses specifically on epilepsy and incorporates clinically relevant state variables such as seizure severity and side effects. 

Solution Method:
We modeled this project system as a Markov Decision Process (MDP) and compute decisions using both a policy and a value iteration approach, then evaluated these policies through simulation. We also incorporated partial observability by modeling noisy patient observations. The observed seizure levels and side effects may differ slightly from the true state. In order to handle this uncertainty, we implemented a particle filter to estimate the true patient state based on observations over time. 

The objective was to maximize long-term patient well-being, which includes many confounding variables such as seizure frequency, severity level, excessive treatment duration, as well as rewards such as seizure reduction and minimized side-effect states. Using this framework, we computed policies that recommend the best action for each state.

Implemenation of Solution Method:
(Just a quick overview of our code): We implemented this system as a simulation of patient progression over time. the model we used does the following:
  * Represents states as tuples
  * Generates successor states based on chosen actions
  * Samples outcomes using probabilistic transitions
  * Evaluates decisions using a reward function
  * Computes optimal policies using value iteration and policy iteration, and then evaluates them through simulation

We represented states as a tuple storing seizure level, treatment stage, side effects, and time in current stage. The transition function explictly defines probabilistic outcomes for each action. For example, increasing dosage has a higher probability of improving seizures but also introduces a higher probability of worsening side effects.

Our reward function then penalizes frequent seizure levels and severe side effects and rewards improvement in patient condition. Then our policy computation evaluates actions over time and selects those that maximize the expected reward.

We evaluated our policies by running simulations of patient outcomes over time, by tracking total reward, state transitions, and observed outcomes. this allowed us to compare how different policies perform in realistic, stochastic scenarios. 

We are very limited in this work due to a simplified state space (it is difficult to model real patients) and by not having any real clinical data. 

[^1]: Steimle, L. N., & Denton, B. T. (n.d.). Markov Decision Processes for Screening and Treatment of Chronic Diseases 


Work disrtibution Statements:

#################### MZK #######################
I formulated the epilepsy outpatient management problem as a finite Markov Decision Process (MDP) grounded in real-world clinical data. The state space was defined to reflect clinically meaningful patient statuses at each visit, incorporating seizure frequency (discretized into ordinal categories), medication side-effect burden (none, mild, moderate, severe), and treatment stage (e.g., monotherapy, dual therapy, refractory/polytherapy). Additional covariates such as adherence and comorbidities were incorporated where data completeness allowed, ensuring that each state captured a realistic snapshot of patient condition at the time of decision-making.

The action space consisted of clinically relevant interventions available during an outpatient visit, including maintaining the current regimen, escalating therapy (dose increase or additional antiseizure medication), de-escalating therapy, or switching medications. Transition probabilities between states were empirically estimated from longitudinal outpatient data, using observed frequencies of changes in seizure control and side-effect profiles following each intervention. Where data sparsity existed, I applied smoothing techniques and clinically informed constraints to maintain plausible transition dynamics.

The reward function was designed to reflect real-world clinical priorities by balancing seizure reduction against treatment tolerability. Positive rewards were assigned to transitions resulting in improved seizure control (e.g., reduction in seizure frequency category), while penalties were applied for worsening seizures or increased side-effect burden. Additional weighting was introduced to reflect the higher clinical importance of achieving seizure freedom relative to incremental improvements, as well as the negative impact of severe adverse effects on quality of life. This formulation enabled the model to capture the inherent trade-offs clinicians face between efficacy and tolerability.

Overall, this MDP framework allowed me to model outpatient epilepsy management as a sequential decision-making process under uncertainty, directly informed by real clinical data and aligned with practical treatment considerations.


##################### Tessa Spitz ####################
I helped to model the transition and reward functions as well as the overall MDP functions. A lot of the initial work was done by MZK (as was his idea), and then I helped implement the state and actions spaces that he designed. Then Aurora and I typed up the final report that demonstrates how we did this, what our problem was and how we went about solving it, and also some of our results. Overall, I think the work was distributed evenly.
