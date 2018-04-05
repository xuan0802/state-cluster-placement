import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from constants import *
from availability_calculation import add_node, cal_avail


def run(input_topo):
    """run availability greedy algorithms"""
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
        # sort centers, zones, servers according to total availability
        A_ = []
        for d in DC_:
            for z in AZ[d]:
                for s in SV[d, z]:
                    A_.append((d, z, s))
            A_.sort(key=lambda x: Ad[x[0]]*Adz[x[0], x[1]]*Adzs[x[0], x[1], x[2]], reverse=True)
        # place standby until the availability threshold is met
        stb_i = 0
        stop = 0
        av_tree = {}
        A_d = []
        A_zs = {}

        for d, z, s in A_:
            if d not in A_d:
                A_d.append(d)
                A_zs[d] = []
                A_zs[d].append((z, s))
            else:
                A_zs[d].append((z, s))

        for d in A_d:
            for z, s in A_zs[d]:
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
                        break
                else:
                    # if server already used, check another server
                    continue
            # decrease link bandwidth if there is any standby
            if stb_i > 0:
                BW[active, d] = BW[active, d] - BWR[active]
            # if availability satisfied, stop placement
            if stop:
                print(avail_r)
                break
        if not stop:
            print("availability greedy model infeasible")
            print("can't place for active at %s" % active)
            quit()
    return standby
