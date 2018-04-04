
from init_topo import initialize_input
from algorithms import bandwidth_greedy, zone_aware, avail_greedy
from ultilities import print_placement

if __name__ == '__main__':
    input_topo = initialize_input()
    result = bandwidth_greedy.run(input_topo)
    print_placement(result)
    print("----------------------")
    input_topo1 = initialize_input()
    result1 = zone_aware.run(input_topo1)
    print_placement(result1)
    print("----------------------")
    input_topo2 = initialize_input()
    result2 = avail_greedy.run(input_topo2)
    print_placement(result2)


