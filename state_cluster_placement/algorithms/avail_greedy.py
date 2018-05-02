import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from state_cluster_placement.constants import *
from state_cluster_placement.availability_calculation import add_node, cal_avail


def run(input_topo, A_min, session_req_rate, ue_num, handover_frequency):
    """run availability greedy algorithms"""
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

    # init solution
    standby = []

    # run algorithm
    # place standby for each active function
    for active in DC:
        satisfied_latency_dc_list = []
        # select centers satisfying latency constraint
        for d in DC:
            if L[d, RN[active]] <= L_max:
                satisfied_latency_dc_list.append(d)
        # sort centers, zones, servers according to total availability
        avail_sorted_dc_az_sv_list = []
        for d in satisfied_latency_dc_list:
            for z in AZ[d]:
                for s in SV[d, z]:
                    avail_sorted_dc_az_sv_list.append((d, z, s))
            avail_sorted_dc_az_sv_list.sort(key=lambda x: Ad[x[0]]*Adz[x[0], x[1]]*Adzs[x[0], x[1], x[2]], reverse=True)
        # place standby until the availability threshold is met
        stb_i = 0
        stop = 0
        av_tree = {}

        for d, z, s in avail_sorted_dc_az_sv_list:
            # check the whether server already was used
            exist = False
            for s_ in standby:
                if s_['location'] == (d, z, s):
                    exist = True
                    break
            # if server not used
            if not exist:
                # resources are enough
                if (C[d] > RD[active]) and (BW[active, d] > BWR[active] + BWT[active, d]):
                    # add standby to solution
                    standby.append({'act': active, 'stb_i': stb_i, 'location': (d, z, s)})
                    # remove server out of data center
                    SV[d, z].remove(s)
                    # decrease compute resources
                    C[d] = C[d] - RD[active]
                    stb_i = stb_i + 1
                    # decrease link bandwidth
                    BW[active, d] = BW[active, d] - BWR[active]
                    BW[d, active] = BW[d, active] - BWR[active]
                    # add into availability tree
                    add_node(d, z, s, av_tree, Ad[d], Adz[d, z], Adzs[d, z, s])
                    # if total availability over threshold, then stop place standby
                    avail_r = cal_avail(av_tree)
                    if avail_r > A_min:
                        stop = True
                        # if availability satisfied, stop placement
                        break
                else:
                    # if not enough resources, check another center
                    continue

            else:
                # if not exist, check another
                continue

            # if availability satisfied, stop placement
            if stop:
                print(avail_r)
                break
        if not stop:
            print("availability greedy model infeasible")
            print("can't place for active at %s" % active)
    return standby
