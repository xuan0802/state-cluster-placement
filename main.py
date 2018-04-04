
from init_topo import initialize_input
from algorithms import bandwidth_greedy, zone_aware, avail_greedy
from ultilities import print_placement
from evaluation import evaluate

if __name__ == '__main__':
    print("------------bandwidth greedy----------")
    input_topo = initialize_input()
    placement_result = bandwidth_greedy.run(input_topo)
    print(evaluate(placement_result, input_topo))
    print("------------zone aware---------------")
    input_topo1 = initialize_input()
    placement_result1 = zone_aware.run(input_topo1)
    print(evaluate(placement_result1, input_topo1))
    print("------------availability greedy-----")
    input_topo2 = initialize_input()
    placement_result2 = avail_greedy.run(input_topo2)
    print(evaluate(placement_result2, input_topo2))


