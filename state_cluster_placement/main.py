
from state_cluster_placement.topos import random_topo
from state_cluster_placement.algorithms import bandwidth_greedy, zone_greedy, avail_greedy, zone_aware
from state_cluster_placement.evaluation import evaluate
from state_cluster_placement.ultilities import save_to_file, load_topo, draw_bar_chart
from copy import deepcopy
from state_cluster_placement.constants import *


if __name__ == '__main__':
    """run all algorithms and make plots"""
    # # create a random topology
    # input_topo = random_topo.initialize_input()
    # # save topo in a file
    # save_to_file(input_topo, "topo_json/topo.json")
    # # load topo from a file
    topo = load_topo("topo_json/topo.json")

    # obtain plot data
    A_min_list = [0.99, 0.999, 0.9995]
    # create dict to store performance data
    bw_gr = dict()
    bw_gr['label'] = "BWGR"
    av_gr = dict()
    av_gr['label'] = "AVGR"
    zo_gr = dict()
    zo_gr['label'] = "ZOGR"
    zo_aw = dict()
    zo_aw['label'] = "ZOAW"
    # each algo dict contains label, lists of results for each kind performance metric
    for data in TITLE_DATA_MAP.values():
        bw_gr[data] = list()
        av_gr[data] = list()
        zo_gr[data] = list()
        zo_aw[data] = list()

    # vary availability min and run algorithms
    for a_m in A_min_list:
        print(a_m)
        print("------------bandwidth greedy----------")
        # make a deep copy of topo
        input_topo0 = deepcopy(topo)
        # run algorithm
        placement_result0 = bandwidth_greedy.run(input_topo0, a_m)
        # calculate performance metrics
        perf0 = evaluate(placement_result0, topo)
        print(perf0)
        # store into a dict
        bw_gr['aver_avail'].append(perf0['aver_avail'])
        bw_gr['num_stb_total'].append(perf0['num_stb_total'])
        bw_gr['total_bw'].append(perf0['total_bw'])

        print("------------zone greedy---------------")
        input_topo1 = deepcopy(topo)
        placement_result1 = zone_greedy.run(input_topo1, a_m)
        perf1 = evaluate(placement_result1, topo)
        print(perf1)
        zo_gr['aver_avail'].append(perf1['aver_avail'])
        zo_gr['num_stb_total'].append(perf1['num_stb_total'])
        zo_gr['total_bw'].append(perf1['total_bw'])

        print("------------availability greedy-----")
        input_topo2 = deepcopy(topo)
        placement_result2 = avail_greedy.run(input_topo2, a_m)
        perf2 = evaluate(placement_result2, topo)
        print(perf2)
        av_gr['aver_avail'].append(perf2['aver_avail'])
        av_gr['num_stb_total'].append(perf2['num_stb_total'])
        av_gr['total_bw'].append(perf2['total_bw'])

        print("------------zone aware-------------")
        input_topo3 = deepcopy(topo)
        placement_result3 = zone_aware.run(input_topo3, a_m)
        perf3 = evaluate(placement_result3, topo)
        print(perf3)
        zo_aw['aver_avail'].append(perf3['aver_avail'])
        zo_aw['num_stb_total'].append(perf3['num_stb_total'])
        zo_aw['total_bw'].append(perf3['total_bw'])

    # create plots
    # create list of ticks on x axis
    xtick = list()
    for a in A_min_list:
        xtick.append('a = ' + str(a))

    title_list = ['Average availability', 'Total number of standbys', 'Total bandwidth usage']
    for title in title_list:
        draw_bar_chart(xtick, title, bw_gr, av_gr, zo_gr, zo_aw)
