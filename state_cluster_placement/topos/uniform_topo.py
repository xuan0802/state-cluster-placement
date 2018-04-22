from state_cluster_placement.constants import *

N_DC = 10
N_RN = 10
N_AZ = 5
N_SV =100
C_SV = 200

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
    for d in DC:
        AZ[d] = []
        for i in range(N_AZ):
            AZ[d].append(d + 'az' + str(i))
    for d in DC:
        for z in AZ[d]:
            SV[(d, z)] = []
            for i in range(N_SV):
                SV[(d, z)].append(z + 'sv' + str(i))
    for i in range(N_RN):
        RN['dc' + str(i)] = 'rn' + str(i)

    # init resource capacity
    for d in DC:
        C[d] = N_AZ*N_SV*C_SV

    # init resource demand
    for d in DC:
        RD[d] = 100

    # init latency matrix
    for d in DC:
        for n in RN.values():
            L[(d, n)] = 100

    # init link bandwidth
    for d in DC:
        for d_ in DC:
            if d != d_:
                BW[(d, d_)] = 40
            else:
                BW[(d, d_)] = 100

    # init bandwidth consumption for state replication and transfer
    for d in DC:
        BWR[d] = 5
        for d_ in DC:
            if d != d_:
                BWT[(d, d_)] = 10
            else:
                BWT[(d, d_)] = 0

    # init availability tree
    for d in DC:
        Ad[d] = 0.9999
        for z in AZ[d]:
            Adz[(d, z)] = 0.999
            for s in SV[(d, z)]:
                Adzs[(d, z, s)] = 0.99

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
