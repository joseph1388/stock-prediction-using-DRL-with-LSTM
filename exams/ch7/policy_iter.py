import numpy as np

from snake import SnakeEnv, TableAgent, eval_game

policy_ref = [1] * 97 + [0] * 3
policy_0 = [0] * 100
policy_1 = [1] * 100

def test_easy():
    np.random.seed(0)
    sum_opt = 0
    sum_0 = 0
    sum_1 = 0
    env = SnakeEnv(0, [3, 6])
    for i in range(10000):
        sum_opt += eval_game(env, policy_ref)
        sum_0 += eval_game(env, policy_0)
        sum_1 += eval_game(env, policy_1)
    print 'opt avg={}'.format(sum_opt / 10000.0)
    print '0 avg={}'.format(sum_0 / 10000.0)
    print '1 avg={}'.format(sum_1 / 10000.0)

class PolicyIteration(object):

    def policy_evaluation(self, agent, max_iter = -1):
        iteration = 0
        # iterative eval
        while True:
            # one iteration
            iteration += 1
            new_value_pi = agent.value_pi.copy()
            for i in range(1, agent.s_len): # for each state
                value_sas = []
                ac = agent.pi[i]
                # for j in range(0, agent.act_num): # for each act
                # print ac
                transition = agent.p[ac, i, :]
                value_sa = np.dot(transition, agent.r + agent.gamma * agent.value_pi)
                    # value_sas.append(value_sa)
                new_value_pi[i] = value_sa# value_sas[agent.policy[i]]
            diff = np.sqrt(np.sum(np.power(agent.value_pi - new_value_pi, 2)))
            # print 'diff={}'.format(diff)
            if diff < 1e-6:
                break
            else:
                agent.value_pi = new_value_pi
            if iteration == max_iter:
                break

    def policy_improvement(self, agent):
        new_policy = np.zeros_like(agent.pi)
        for i in range(1, agent.s_len):
            for j in range(0, agent.a_len):
                agent.value_q[i,j] = np.dot(agent.p[j,i,:], agent.r + agent.gamma * agent.value_pi)
                # update policy
            max_act = np.argmax(agent.value_q[i,:])
            new_policy[i] = max_act
        if np.all(np.equal(new_policy, agent.pi)):
            return False
        else:
            agent.pi = new_policy
            return True

    def policy_iteration(self, agent):
        iteration = 0
        while True:
            iteration += 1
            self.policy_evaluation(agent)
            ret = self.policy_improvement(agent)
            if not ret:
                break
        print 'Iter {} rounds converge'.format(iteration)


def policy_iteration_demo1():
    env = SnakeEnv(0, [3,6])
    agent = TableAgent(env)
    pi_algo = PolicyIteration()
    pi_algo.policy_iteration(agent)
    print 'return_pi={}'.format(eval_game(env, agent))
    print agent.pi

def policy_iteration_demo2():
    env = SnakeEnv(10, [3,6])
    agent = TableAgent(env)
    agent.pi[:]=0
    print 'return3={}'.format(eval_game(env,agent))
    agent.pi[:]=1
    print 'return6={}'.format(eval_game(env,agent))
    agent.pi[97:100]=0
    print 'return_ensemble={}'.format(eval_game(env,agent))
    pi_algo = PolicyIteration()
    pi_algo.policy_iteration(agent)
    print 'return_pi={}'.format(eval_game(env,agent))
    print agent.pi

if __name__ == '__main__':
    # test_easy()
    policy_iteration_demo1()
    policy_iteration_demo2()


