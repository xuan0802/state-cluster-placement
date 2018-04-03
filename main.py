
from init_topo import initialize_input
from algorithms import bandwidthgreedy, zone_aware
from ultilities import print_placement

if __name__ == '__main__':
    input_topo = initialize_input()
    result = bandwidthgreedy.run(input_topo)
    print_placement(result)
    print("----------------------")
    input_topo1 = initialize_input()
    result1 = zone_aware.run(input_topo1)
    print_placement(result1)



