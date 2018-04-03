import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import *
from availability_calculation import add_node, cal_avail


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
    N_STB = 0
    standby = {}

    # run algorithm
    # place standby for each active function
    for active in DC:
        DC_ = []
        # select centers satisfying latency constraint
        for d in DC:
            if L[d, RN[active]] <= L_max:
                DC_.append(d)
        # sort selected centers according to bandwidth
        DC_.sort(key = lambda x: BW[active,x])
        # sort zones, servers according to total availability
        A_ = {}
        for d in DC_:
            A_[d] = []
            for z in AZ[d]:
                for s in SV[d, z]:
                    A_[d].append((z,s))
            A_[d].sort(key = lambda x: Adz[d,x[0]]*Adzs[d,x[0],x[1]], reverse= True)
        # place standby until the availability threshold is met
        i = 0
        stop = 0
        av_tree = {}
        for d in DC_:
            for z,s in A_[d]:
                if (C[d] > RD[active]) and (BW[active, d] > BWR[active] + BWT[active, d]):
                    print(z,s)
                    standby[(active, i+1),(d,z,s)] = 1
                    C[d] = C[d] - RD[active]
                    i = i + 1
                    # add into availability tree
                    add_node(d, z, s, av_tree, Ad[d], Adz[d, z], Adzs[d, z, s])
                    # if total availability over threshold, then stop place standby
                    print(cal_avail(av_tree))
                    if cal_avail(av_tree) > A_min:
                        stop = 1
                        break
                else:
                    break
            if stop == 1:
                if i > 0:
                    BW[active, d] = BW[active, d] - BWR[active]
                break
        if not stop:
            print("model infeasible")
            quit()
    return standby
