import pickle
import torch
import matplotlib.pyplot as plt

from DRL.dqn_agent import Agent
from agents.statics import action_BUY
from environments.DayByDayEnvironment import DayByDayEnvironment


def choose_action(state):

    action = agent.act(state, eps=0)

    return action

SYMBOL = "SPCE"

with open("../data/"+SYMBOL+"/intraday.pckl", "rb") as fb:
    _intraday = pickle.load(fb)

    intraday = []
    for H in list(enumerate(_intraday['intraday'].items())):
        _, t = H
        d, i = t
        v = [d, float(i['open']), float(i['close']), float(i['high']), float(i['close']), int(i['volume'])]
        intraday.append(v)

    intraday = [a for a in reversed(intraday)]

original_money = 1000
money = original_money

env = DayByDayEnvironment(intraday, market_cap=0, money=money, delta = 0.01)
action_space = env.get_action_space()
state_space  = env.get_state_space()

state = env.get_state_space()
action_dict = {-1:0, 0:0, 1:0}

agent = Agent(state_size=state_space, action_size=action_space, seed=1,  fc1_neurons=64, fc2_neurons=64)

agent.load_model(SYMBOL+'_daily_trader.pt')

for step in range(len(intraday)):
    state = env.make_state_from_history(step)
    action = choose_action(state)
    action_dict[action] += 1
    if action == action_BUY and money <= 1:
        pass
    else:
        reward, next_state, done, info = env.step(action)
        state = next_state
        money = info['money']
        stock = info['stock']

print(action_dict, money, stock)
