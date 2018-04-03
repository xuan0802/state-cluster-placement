from constants import *
from init_topo import initialize_input
from algorithms import bandwidthgreedy
import json

if __name__ == '__main__':
    input_topo = initialize_input()
    result = bandwidthgreedy.run(input_topo)
    print(json.dumps(result))