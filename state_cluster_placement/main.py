
from state_cluster_placement.topos import random_topo
from state_cluster_placement.algorithms import bandwidth_greedy, zone_aware, avail_greedy
from state_cluster_placement.evaluation import evaluate
from matplotlib import pyplot as plt
from state_cluster_placement.ultilities import save_topo, load_topo

if __name__ == '__main__':
    """run all algorithms and make plots"""
    # create a random topology
    input_topo = random_topo.initialize_input()
    # save topo in a file
    save_topo(input_topo, "topo.json")
    # load topo from a file
    topo = load_topo("topo.json")

    print("------------bandwidth greedy----------")
    input_topo0 = dict(topo)
    placement_result = bandwidth_greedy.run(input_topo0)
    print(evaluate(placement_result, topo))

    print("------------zone aware---------------")
    input_topo1 = dict(topo)
    placement_result1 = zone_aware.run(input_topo1)
    print(evaluate(placement_result1, topo))

    print("------------availability greedy-----")
    input_topo2 = dict(topo)
    placement_result2 = avail_greedy.run(input_topo2)
    print(evaluate(placement_result2, topo))


    plt.figure()