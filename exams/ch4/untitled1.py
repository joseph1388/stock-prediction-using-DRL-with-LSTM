# -*- coding: utf-8 -*-
"""
Created on Tue May 29 08:10:22 2018

@author: joseph
"""

import gym

test_envs={'algorithm':'Copy-v0',
           'toy_text':'FrozenLake-v0',
           'control':'CartPole-v0', # option：MountainCar-v0
           'atari':'SpaceInvaders-v0',# options：'Breakout-ram-v4'，'Seaquest-v0',
          'mujoco':'Humanoid-v1',     # not feasible on Win10
          'box2d':'LunarLander-v2' }  # not feasible on Win10

game_name = test_envs['algorithm']
env = gym.make(game_name)
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render() 
        print(observation)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
