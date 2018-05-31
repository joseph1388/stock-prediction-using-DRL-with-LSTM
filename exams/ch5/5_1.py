import gym
import sys

env = gym.make(sys.argv[1])
env.reset()
for i in range(1000):
    env.render()
    ob, reward, done, info = env.step(env.action_space.sample())
    if done:
        env.reset()