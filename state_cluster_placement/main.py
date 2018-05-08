
from state_cluster_placement.topos import random_topo
from state_cluster_placement.algorithms import bandwidth_greedy, zone_greedy, avail_greedy, usage_aware
from state_cluster_placement.evaluation import evaluate
from state_cluster_placement.ultilities import save_to_file, load_topo, draw_bar_chart
from copy import deepcopy
from state_cluster_placement.constants import *
from random import choice

if __name__ == '__main__':
    """run all algorithms and make plots"""
    # # create a random topology
    # input_topo = random_topo.initialize_input()
    # # save topo in a file
    # save_to_file(input_topo, "topo_json/topo.json")
    # # load topo from a file
    topo = load_topo("topo_json/topo.json")

    # create resource demand and bandwidth transfer and replication
    session_req_rate_list = [7]
    ue_num_list = [500]
    handover_frequency_list = [1000]
    session_req_rate = {}
    ue_num = {}
    handover_frequency = {}
    for d in topo['DC']:
        session_req_rate[d] = choice(session_req_rate_list)
        ue_num[d] = choice(ue_num_list)
    for d in topo['DC']:
        for d_ in topo['DC']:
            if d != d_:
                handover_frequency[d, d_] = choice(handover_frequency_list)
            else:
                handover_frequency[d, d_] = 0
    # obtain plot data
    A_min_list = [0.99, 0.999, 0.9995]
    # create dict to store performance data
    bw_gr = dict()
    bw_gr['label'] = "BWGR"
    av_gr = dict()
    av_gr['label'] = "AVGR"
    zo_gr = dict()
    zo_gr['label'] = "ZOGR"
    ua_rg = dict()
    ua_rg['label'] = "UARG"
    # each algo dict contains label, lists of results for each kind performance metric
    for data in TITLE_DATA_MAP.values():
        bw_gr[data] = list()
        av_gr[data] = list()
        zo_gr[data] = list()
        ua_rg[data] = list()

    # vary availability min and run algorithms
    for a_m in A_min_list:
        print(a_m)
        print("------------bandwidth greedy----------")
        # make a deep copy of topo
        input_topo0 = deepcopy(topo)
        # run algorithm
        placement_result0 = bandwidth_greedy.run(input_topo0, a_m, session_req_rate, ue_num, handover_frequency)
        # calculate performance metrics
        perf0 = evaluate(placement_result0, topo, session_req_rate, ue_num, handover_frequency)
        print(perf0)
        # store into a dict
        bw_gr['aver_avail'].append(perf0['aver_avail'])
        bw_gr['num_stb_total'].append(perf0['num_stb_total'])
        bw_gr['total_bw'].append(perf0['total_bw'])

        print("------------zone greedy---------------")
        input_topo1 = deepcopy(topo)
        placement_result1 = zone_greedy.run(input_topo1, a_m, session_req_rate, ue_num, handover_frequency)
        perf1 = evaluate(placement_result1, topo, session_req_rate, ue_num, handover_frequency)
        print(perf1)
        zo_gr['aver_avail'].append(perf1['aver_avail'])
        zo_gr['num_stb_total'].append(perf1['num_stb_total'])
        zo_gr['total_bw'].append(perf1['total_bw'])

        print("------------availability greedy-----")
        input_topo2 = deepcopy(topo)
        placement_result2 = avail_greedy.run(input_topo2, a_m, session_req_rate, ue_num, handover_frequency)
        perf2 = evaluate(placement_result2, topo, session_req_rate, ue_num, handover_frequency)
        print(perf2)
        av_gr['aver_avail'].append(perf2['aver_avail'])
        av_gr['num_stb_total'].append(perf2['num_stb_total'])
        av_gr['total_bw'].append(perf2['total_bw'])

        print("------------usage aware-------------")
        input_topo3 = deepcopy(topo)
        placement_result3 = usage_aware.run(input_topo3, a_m, session_req_rate, ue_num, handover_frequency)
        perf3 = evaluate(placement_result3, topo, session_req_rate, ue_num, handover_frequency)
        print(perf3)
        ua_rg['aver_avail'].append(perf3['aver_avail'])
        ua_rg['num_stb_total'].append(perf3['num_stb_total'])
        ua_rg['total_bw'].append(perf3['total_bw'])

    # create plots
    # create list of ticks on x axis
    xtick = list()
    for a in A_min_list:
        xtick.append('A_min = ' + str(a))

    title_list = ['Average availability', 'Total number of standbys', 'Total bandwidth usage (Mbps)']
    for title in title_list:
        draw_bar_chart(xtick, title, bw_gr, av_gr, zo_gr, ua_rg)
