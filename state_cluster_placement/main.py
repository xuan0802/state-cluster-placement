
from state_cluster_placement.topos import random_topo
from state_cluster_placement.algorithms import bandwidth_greedy, zone_aware, avail_greedy
from state_cluster_placement.evaluation import evaluate
from state_cluster_placement.ultilities import save_topo, load_topo, draw_bar_chart
from copy import deepcopy


if __name__ == '__main__':
    """run all algorithms and make plots"""
    # create a random topology
    # input_topo = random_topo.initialize_input()
    # # save topo in a file
    # save_topo(input_topo, "topo.json")
    # # load topo from a file
    topo = load_topo("topo.json")

    # obtain plot data
    A_min_list = [0.9987, 0.9988, 0.9989]
    # create dict to store performance data
    bw_gr = dict()
    bw_gr['label'] = "BWGR"
    bw_gr['data'] = list()
    av_gr = dict()
    av_gr['label'] = "AVGR"
    av_gr['data'] = list()
    za_rg = dict()
    za_rg['label'] = "AZRG"
    za_rg['data'] = list()
    # vary availability min and run algorithms
    for a_m in A_min_list:
        print(a_m)
        print("------------bandwidth greedy----------")
        input_topo0 = deepcopy(topo)
        placement_result0 = bandwidth_greedy.run(input_topo0, a_m)
        perf0 = evaluate(placement_result0, topo)
        print(perf0)
        bw_gr['data'].append(perf0['aver_avail'])

        print("------------zone aware---------------")
        input_topo1 = deepcopy(topo)
        placement_result1 = zone_aware.run(input_topo1, a_m)
        perf1 = evaluate(placement_result1, topo)
        print(perf1)
        za_rg['data'].append(perf1['aver_avail'])

        print("------------availability greedy-----")
        input_topo2 = deepcopy(topo)
        placement_result2 = avail_greedy.run(input_topo2, a_m)
        perf2 = evaluate(placement_result2, topo)
        print(perf2)
        av_gr['data'].append(perf2['aver_avail'])

    # create plots
    xtick = list()
    for a in A_min_list:
        xtick.append('a = ' + str(a))
    draw_bar_chart(xtick, bw_gr, av_gr, za_rg)