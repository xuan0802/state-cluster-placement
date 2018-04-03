
from init_topo import initialize_input
from algorithms import bandwidthgreedy
from ultilities import print_placement

if __name__ == '__main__':
    input_topo = initialize_input()
    result = bandwidthgreedy.run(input_topo)
    print_placement(result)

