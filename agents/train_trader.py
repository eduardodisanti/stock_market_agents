import pickle
import matplotlib.pyplot as plt
import numpy as np
import torch

from DRL.dqn_agent import Agent

from environments.OneDayEnvironment import OneDayEnvironment, action_BUY, action_SELL, action_HOLD


def choose_action(state, epsilon):

    action = agent.act(state, eps=epsilon)

    return action

SYMBOL = "JNJ"

with open("../data/"+SYMBOL+"/intraday.pckl", "rb") as fb:
    _intraday = pickle.load(fb)

    intraday = []
    for H in list(enumerate(_intraday['intraday'].items())):
        _, t = H
        d, i = t
        v = [d, float(i['open']), float(i['close']), float(i['high']), float(i['close']), int(i['volume'])]
        intraday.append(v)

original_money = 1000
stock = 0
money = original_money

env = OneDayEnvironment(intraday, market_cap=0, money=money, delta = 0.01)
action_space = env.get_action_space()
state_space  = env.get_state_space()

state = env.get_state_space()

hist = []
EPS_START = 1  # START EXPLORING A LOT
GAMMA = 0.9999  # discount factor -

BUFFER_SIZE = int(1e3)  # replay buffer size
BATCH_SIZE = 64  # minibatch size
TAU = 1e-3  # for soft update of target parameters
LR = 5e-4  # learning rate
UPDATE_EVERY = 4  # how often to update the network

agent = Agent(state_size=state_space, action_size=action_space, seed=1, gamma=GAMMA, buffer_size=BUFFER_SIZE,
              batch_size=BATCH_SIZE, tau=TAU, lr=LR, update_every=UPDATE_EVERY,  fc1_neurons=64, fc2_neurons=64)

TARGET_AVG_SCORE = 10000
NUM_OF_TARGET_EPISODES_FOR_AVG = 100

eps_min = 0.001  # EVEN EXPLORE AFTER MANY EPISODES
eps_decay = 0.99995  # DECAY EXPLORE SLOWLY
best_score = -1e10

trained = False
episodes = 0
la = {0: 0, 1: 0, 2:0}
lq = []
consecutives_solved = 0
times_solved = 0
avg = 0
mav = 0
avgs = []
mavgs = []

scores = []

eps = EPS_START
behaviour_assess = {-1:0, 0:0, 1:0}

while not trained:
    state = env.reset()  # reset the environment
    score = 0  # initialize the score
    #for trys in range(0,20000):
    next_mark = 10e10
    env.stock = 0
    env.money = original_money

    stock = 0
    money = original_money
    total_assets = 0

    while True:
        #env.render()
        action = choose_action(state, eps)  # select an action
        actual_price = state[1]
        last_assets = money + next_mark * stock
        if action == action_BUY and money * actual_price > 0 or action == action_SELL and stock > 0 or action == action_HOLD:
            la[action] += 1
            reward, next_state, done, info = env.step(action)
            behaviour_assess[reward]+=1
            money = info['money']
            stock = info['stock']
            next_mark = info['next']
            total_assets = money + next_mark * stock
            #score += reward # update the score
            score += total_assets - last_assets
            if done:  # exit loop if episode finished
                break

            agent.step(state, action, reward, next_state, done)
            eps = max(eps_min, eps_decay * eps)
            state = next_state  # roll over the state to next time step

    episodes += 1
    lq.append(score)

    avg = np.average(lq[-NUM_OF_TARGET_EPISODES_FOR_AVG:])
    avgs.append(avg)

    if (len(avgs)%10) == 0:
        plt.plot(avgs, ".", c="b")
        plt.pause(0.1)
        print("act", la, "assess", behaviour_assess)
        print("episodes", episodes, "last score", score, "current eps", eps, "avg", avg, "best", best_score, "money", money, "stock", stock, "next mark", next_mark, "total", total_assets)
        if avg > best_score:
            torch.save(agent.qnetwork_local.state_dict(), 'smart_trader.pt')
            best_score = avg

    if avg > TARGET_AVG_SCORE:
        times_solved += 1
    else:
        consecutives_solved = 0
    if avg > TARGET_AVG_SCORE or episodes > 10000:
        trained = True
        if avg > best_score:
            torch.save(agent.qnetwork_local.state_dict(), 'smart_trader.pt')
        print("Trained")
        print("episodes", episodes, "last score", score, "current eps", eps, "avg", avg, "money", money, "stock", stock, "next mark", next_mark, "assets", total_assets)

print("Score: {}".format(score))