from state_cluster_placement.availability_calculation import add_node, cal_avail
from state_cluster_placement.constants import *

def evaluate(placement, input_topo, session_req_rate, ue_num, handover_frequency):
    """calculate performance values"""
    # get input
    DC = input_topo['DC']
    AZ = input_topo['AZ']
    SV = input_topo['SV']
    RN = input_topo['RN']
    C = input_topo['C']
    L = input_topo['L']
    BW = input_topo['BW']
    Ad = input_topo['Ad']
    Adz = input_topo['Adz']
    Adzs = input_topo['Adzs']

    RD = {}
    BWR = {}
    BWT = {}
    # calculate resource demand, bw transfer and replication
    # resource demand
    for d in DC:
        RD[d] = RD_init + RD_unit*ue_num[d]*session_req_rate[d]
    # bandwidth consumption for state replication and transfer
    for d in DC:
        BWR[d] = ue_num[d]*(BWR_attach + BWR_ses_req*session_req_rate[d])
        for d_ in DC:
            if d != d_:
                BWT[(d, d_)] = handover_frequency[d, d_] * BWT_handover
            else:
                BWT[(d, d_)] = 0

    # create a dict to store performance results
    perf_result = dict()

    # calculate the number of standby functions deployed
    perf_result['num_stb_total'] = len(placement)

    # calculate the average availability
    dict_av_tree = {}
    total_avail = 0
    for active in DC:
        dict_av_tree[active] = {}
        for p in placement:
            if p['act'] == active:
                d = p['location'][0]
                z = p['location'][1]
                s = p['location'][2]
                add_node(d, z, s, dict_av_tree[active],
                         Ad[d], Adz[d, z], Adzs[d, z, s])
    for active in DC:
        total_avail = total_avail + cal_avail(dict_av_tree[active])
    perf_result['aver_avail'] = total_avail/len(DC)

    # calculate total link bandwidth required
    total_bw = 0
    for active in DC:
        for p in placement:
            if active != p['location'][0] and p['act'] == active:
                total_bw = total_bw + BWR[active]
    perf_result['total_bw'] = total_bw

    return perf_result
