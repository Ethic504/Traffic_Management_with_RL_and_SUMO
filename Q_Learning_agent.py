import numpy as np
import gym
import random
import time
from IPython.display import clear_output
import runner as runsumo


env =gym.make("FrozenLake-v0")      
action_space_size = 4 # 4 traffic light 
state_space_size = 100
q_table = np.zeros((state_space_size, action_space_size))
#print(q_table)

num_episodes = 1000             # number of episode
max_steps_per_episode = 5000     # number of step per episode

learning_rate = 0.1             # value of alpha
discount_rate = 0.99            # value of lamda

# efsolon greedy stratagy 
exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

rewards_all_episodes = []

# Q-learning algorithm
for episode in range(num_episodes): # this loop contains everything for a single episode
    
    #runsumo.sumo_config()
    
    state = env.reset() # reset the state of the env after each episode
    #print(state)
    # restart the simulation
    done = False # wheather our episode is finished
    rewards_current_episode = 0 # reword with in the current episode and for every new episode it sets to 0 and get updated in the episode loop
    
    for step in range(max_steps_per_episode): # this loop contains everything for a single step
        
        # Exploreation-exploitation trade-off
        exploration_rate_threshold = random.uniform(0, 1) # set the exploration thrasehold random in between 0 to 1, this will help the agent so take decission for going exploration or exploatation 
        if exploration_rate_threshold > exploration_rate: # agent will exploite the environment 
            action = np.argmax(q_table[state,:]) # and will choose the max value for the action from the Q-table
        else: # agent will explore the environment 
            action = env.action_space.sample() # and sample an action randomly/takes new action
            #print('printing action : ',action)
        #print(state, action)
        new_state, reward, done, info = env.step(action) #  it return a tuple by performing the action desided before and along with 4 variable from the environment
        
        # Update Q-table for Q(s,a)
        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))
           
        state = new_state # setting current sate to new state
        #print(state)
        rewards_current_episode += reward # update the reward after the action taken place
        
        if done == True: # check if the last action ended the episode
            break # if yes then the step loop will over and new episode will start
        #print(state)
        
        
    # Exploration rate decay
    exploration_rate = min_exploration_rate + \
        (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
        
    rewards_all_episodes.append(rewards_current_episode) # update the reward list for each episode
        
# # Calculate and print the average reward per thousand episodes
# rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes),num_episodes/1000)
# #print(len(rewards_per_thousand_episodes))
# count = 1000
# print("************Average reward per thousand episodes**************\n")
# for r in rewards_per_thousand_episodes:
#     #print(count, ': ', str(sum(r/1000)))
#     count = count + 1000
    
# # print update Q-table
# print("\n\n*****Q-table*****\n")
# print(q_table)        
        
            