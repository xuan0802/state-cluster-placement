import ujson
from ast import literal_eval

def print_placement(placement):
    """print placement nicely"""
    placement.sort(key=lambda x: x['act'])
    for p in placement:
        print(p)


def save_topo(input_topo, filename):
    """save topo to a json file"""
    f = open(filename, "w")
    ujson.dump(input_topo, f)
    f.close()


def load_topo(filename):
    # load topo from a file
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

    f = open(filename)
    topo = ujson.load(f)
    f.close()
    DC = topo['DC']
    for i in topo['AZ'].keys():
        AZ[i] = topo['AZ'][i]
    for i in topo['SV'].keys():
        SV[literal_eval(i)] = topo['SV'][i]
    for i in topo['RN'].keys():
        RN[i] = topo['RN'][i]
    for i in topo['C'].keys():
        C[i] = topo['C'][i]
    for i in topo['L'].keys():
        L[literal_eval(i)] = topo['L'][i]
    for i in topo['BW'].keys():
        BW[literal_eval(i)] = topo['BW'][i]
    for i in topo['RD'].keys():
        RD[i] = topo['RD'][i]
    for i in topo['BWR'].keys():
        BWR[i] = topo['BWR'][i]
    for i in topo['BWT'].keys():
        BWT[literal_eval(i)] = topo['BWT'][i]
    for i in topo['Ad'].keys():
        Ad[i] = topo['Ad'][i]
    for i in topo['Adz'].keys():
        Adz[literal_eval(i)] = topo['Adz'][i]
    for i in topo['Adzs'].keys():
        Adzs[literal_eval(i)] = topo['Adzs'][i]

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
