import pickle
import matplotlib.pyplot as plt

from environments.AbstractEnvironment import action_BUY
from environments.FullHistoryEnvironment import OneDayEnvironment

def choose_action(state):
    action = env.sample()

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
money = original_money

env = OneDayEnvironment(intraday, market_cap=0, money=money, delta = 0.01)
action_space = env.get_action_space().shape[0]
state_space  = env.get_state_space().shape[0]

state = env.get_state_space()
action_dict = {1:0, -1:0, 0:0}
hist = []
for i in range(1000000):
    action = choose_action(state)
    action_dict[action] += 1
    if action == action_BUY and money < 0:
        pass
    else:
        reward, next_state, done, info = env.step(action)
        state = next_state
        money = info['money']
        if done:
            env.reset()
            state = env.get_state_space()
            hist.append(money - original_money)
            money = original_money
        #print("action", action, "money", money)

print(action_dict, money)
plt.hist(hist)
plt.show()