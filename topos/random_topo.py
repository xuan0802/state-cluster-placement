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
    for d in DC:
        AZ[d] = []
        N_AZ = randint(3, 8)
        for i in range(N_AZ):
            AZ[d].append('az' + str(i))
    for d in DC:
        for z in AZ[d]:
            SV[(d, z)] = []
            N_SV = randint(10, 100)
            for i in range(N_SV):
                SV[(d, z)].append('sv' + str(i))

    for i in range(N_RN):
        RN['dc' + str(i)] = 'rn' + str(i)

    # init resource capacity
    C_SV = randint(5, 50)
    for d in DC:
        C[d] = N_AZ*N_SV*C_SV

    # init resource demand
    for d in DC:
        RD[d] = 100

    # init latency matrix
    for d in DC:
        for n in RN.values():
            L[(d, n)] = randint(150, 250)

    # init link bandwidth
    for d in DC:
        for d_ in DC:
            if d != d_:
                BW[(d, d_)] = randint(0, 1000)
            else:
                BW[(d, d_)] = 1000

    # init bandwidth consumption for state replication and transfer
    for d in DC:
        BWR[d] = randint(100, 150)
        for d_ in DC:
            if d != d_:
                BWT[(d, d_)] = 200
            else:
                BWT[(d, d_)] = 0

    # init availability tree
    for d in DC:
        Ad[d] = 0.98 + random()/100
        for z in AZ[d]:
            Adz[(d, z)] = 0.98 + random()/100
            for s in SV[(d, z)]:
                Adzs[(d, z, s)] = 0.98

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
