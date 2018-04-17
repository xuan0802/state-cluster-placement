import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from state_cluster_placement.constants import *
from state_cluster_placement.availability_calculation import add_node, cal_avail


def run(input_topo):
    """run bandwidth greedy algorithms"""
    # get input
    DC = input_topo['DC']
    AZ = input_topo['AZ']
    SV = input_topo['SV']
    RN = input_topo['RN']
    C = input_topo['C']
    L = input_topo['L']
    BW = input_topo['BW']
    RD = input_topo['RD']
    BWR = input_topo['BWR']
    BWT = input_topo['BWT']
    Ad = input_topo['Ad']
    Adz = input_topo['Adz']
    Adzs = input_topo['Adzs']

    # init solution
    standby = []

    # run algorithm
    # place standby for each active function
    for active in DC:
        DC_ = []
        # select centers satisfying latency constraint
        for d in DC:
            if L[d, RN[active]] <= L_max:
                DC_.append(d)
        # sort selected centers according to bandwidth
        DC_.sort(key=lambda x: BW[active, x])
        # sort zones, servers according to total availability
        A_ = {}
        for d in DC_:
            A_[d] = []
            for z in AZ[d]:
                for s in SV[d, z]:
                    A_[d].append((z, s))
            A_[d].sort(key=lambda x: Adz[d, x[0]]*Adzs[d, x[0], x[1]], reverse=True)
        # place standby until the availability threshold is met
        stb_i = 0
        stop = 0
        av_tree = {}
        d_has_stb = []

        for d in DC_:
            for z, s in A_[d]:
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
                        # decrease compute resources
                        C[d] = C[d] - RD[active]
                        stb_i = stb_i + 1
                        # decrease link bandwidth
                        if d not in d_has_stb:
                            d_has_stb.append(d)
                            BW[active, d] = BW[active, d] - BWR[active]
                        # add into availability tree
                        add_node(d, z, s, av_tree, Ad[d], Adz[d, z], Adzs[d, z, s])
                        # if total availability over threshold, then stop place standby
                        avail_r = cal_avail(av_tree)
                        if avail_r > A_min:
                            # if availability satisfied, stop placement
                            stop = True
                            break
                    else:
                        # if not enough resources, check another center
                        break
                else:
                    # if server already used, check another server
                    continue
            # if availability satisfied, stop placement
            if stop:
                break
        if not stop:
            print("bandwidth greedy model infeasible")
            print("can't place for active at %s" % active)
    return standby

