from state_cluster_placement.availability_calculation import add_node, cal_avail


def evaluate(placement, input_topo):
    """calculate performance values"""
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
    dict_location = {}
    for active in DC:
        dict_location[active] = []
        for p in placement:
            if p['location'][0] not in dict_location[active]:
                dict_location[active].append(p['location'][0])
    for active in DC:
        for d in dict_location[active]:
            if active != d:
                total_bw = total_bw + BWR[active]
    perf_result['total_bw'] = total_bw

    return perf_result
