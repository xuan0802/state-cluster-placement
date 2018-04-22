from random import *

N_DC = 10
N_RN = 10


def initialize_input():
    DC = []
    AZ = {}
    SV = {}
    RN = {}
    C = {}
    L = {}
    BW = {}
    RD = {}
    BWR = {}
    BWT = {}
    Ad = {}
    Adz = {}
    Adzs = {}

    # init set of cloud centers, zones, servers, radio nodes
    for i in range(N_DC):
        DC.append('dc' + str(i))
        zone_num_list = [2, 3, 5]
    for d in DC:
        AZ[d] = []
        N_AZ = choice(zone_num_list)
        for i in range(N_AZ):
            AZ[d].append(d + 'az' + str(i))
    for d in DC:
        for z in AZ[d]:
            SV[(d, z)] = []
            server_num_list = [20, 30, 50, 100]
            N_SV = choice(server_num_list)
            for i in range(N_SV):
                SV[(d, z)].append(z + 'sv' + str(i))

    for i in range(N_RN):
        RN['dc' + str(i)] = 'rn' + str(i)

    # init resource capacity
    center_capacity_list = [1000, 1500, 2500, 5000]
    for d in DC:
        C[d] = choice(center_capacity_list)

    # init resource demand
    for d in DC:
        RD[d] = randint(10, 20)

    # init latency matrix
    for d in DC:
        for n in RN.values():
            if n == RN[d]:
                # set low latency for center and its assigned
                # radio nodes to satisfy latency requirement
                L[d, n] = 150
            else:
                # to not assigned radio nodes --> set randomly
                L[(d, n)] = randint(150, 250)

    # init link bandwidth
    link_bw_list = [100, 500, 1000, 2000, 5000, 10000]
    for d in DC:
        for d_ in DC:
            if d != d_:
                if (d, d_) in BW.keys():
                    BW[d, d_] = BW[d_, d]
                else:
                    BW[(d, d_)] = choice(link_bw_list)
            else:
                BW[(d, d_)] = 20000

    # init bandwidth consumption for state replication and transfer
    bwr_list = [100, 150, 200]
    bwt_list = [10, 20, 50, 100]
    for d in DC:
        BWR[d] = choice(bwr_list)
        for d_ in DC:
            if d != d_:
                BWT[(d, d_)] = choice(bwt_list)
            else:
                BWT[(d, d_)] = 0

    # init availability tree
    avail_list = [0.9, 0.99, 0.999]
    for d in DC:
        Ad[d] = choice(avail_list)
        for z in AZ[d]:
            Adz[(d, z)] = choice(avail_list)
            for s in SV[(d, z)]:
                Adzs[(d, z, s)] = choice(avail_list)

    # create input data
    input = dict()
    input['DC'] = DC
    input['AZ'] = AZ
    input['SV'] = SV
    input['RN'] = RN
    input['C'] = C
    input['L'] = L
    input['BW'] = BW
    input['BWR'] = BWR
    input['BWT'] = BWT
    input['RD'] = RD
    input['Ad'] = Ad
    input['Adz'] = Adz
    input['Adzs'] = Adzs
    return input
