import sys, os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from state_cluster_placement.constants import *
from state_cluster_placement.availability_calculation import add_node, cal_avail


def run(input_topo, A_min, session_req_rate, ue_num, handover_frequency):
    """run zone aware algorithms"""
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
                BWT[(d, d_)] = handover_frequency[d, d_]*BWT_unit
            else:
                BWT[(d, d_)] = 0

    # init solution
    standby = []
    # build a use tracking tree
    used_tree = build_use_tracking_tree(DC, AZ, SV, Ad, Adz, Adzs, L, RN)
    # run algorithm
    # place standby for each active function
    for active in DC:
        # reset used tree
        for dc in used_tree['child_nodes']:
            dc['used_child_num'] = 0
            for az in dc['child_nodes']:
                az['used_child_num'] = 0
        stb_i = 0
        stop = False
        av_tree = {}
        # check used tree to place standby function
        while not stop and len(used_tree['child_nodes']) != 0:
            # select centers satisfying latency constraint
            satisfied_latency_dc_list = list()
            for dc in used_tree['child_nodes']:
                if dc['latency'][RN[active]] <= L_max:
                    satisfied_latency_dc_list.append(dc)
            # arrange dc list according to used child num
            satisfied_latency_dc_list.sort(key=lambda x: x['used_child_num'])
            # create a list of dc which have min used child num
            min_used_child_num_dc = satisfied_latency_dc_list[0]['used_child_num']
            min_dc_list = list()
            for dc in used_tree['child_nodes']:
                if dc['used_child_num'] == min_used_child_num_dc:
                    min_dc_list.append(dc)
            # create a list of zones with min used child num
            az_list = list()
            for dc in min_dc_list:
                az_list = az_list + dc['child_nodes']
            az_list.sort(key=lambda x: x['used_child_num'])
            min_used_child_num_az = az_list[0]['used_child_num']
            min_az_list = list()
            for az in az_list:
                if az['used_child_num'] == min_used_child_num_az:
                    min_az_list.append(az)
            # select server with highest availability
            sv_list = list()
            for az in min_az_list:
                sv_list = sv_list + az['child_nodes']
            sv_list.sort(key=lambda x: x['availability'], reverse=True)
            s = sv_list[0]['name']
            z = sv_list[0]['parent_node']['name']
            d = sv_list[0]['parent_node']['parent_node']['name']
            #  check resources whether are enough
            if (C[d] > RD[active]) and (BW[active, d] > BWR[active] + BWT[active, d]):
                # add standby to solution
                standby.append({'act': active, 'stb_i': stb_i, 'location': (d, z, s)})
                # increase used child num
                sv_list[0]['parent_node']['used_child_num'] += 1
                sv_list[0]['parent_node']['parent_node']['used_child_num'] += 1
                # remove server out of used tree
                sv_list[0]['parent_node']['child_nodes'].remove(sv_list[0])
                # decrease compute resources, bandwidth resources
                C[d] = C[d] - RD[active]
                stb_i = stb_i + 1
                BW[active, d] = BW[active, d] - BWR[active]
                BW[d, active] = BW[d, active] - BWR[active]
                # add into availability tree
                add_node(d, z, s, av_tree, Ad[d], Adz[d, z], Adzs[d, z, s])
                # if total availability over threshold, then stop place standby
                avail_r = cal_avail(av_tree)
                if avail_r > A_min:
                    stop = True
                    break
            else:
                # if not enough resources, check another server
                # remove center out of used tree
                for dc in used_tree['child_nodes']:
                    if dc['name'] == d:
                        del used_tree['child_nodes'][used_tree['child_nodes'].index(dc)]
                        break
                continue
        # if availability satisfied, stop placement
        if stop:
            continue
        else:
            print("zone aware model infeasible")
            print("can't place for active at %s" % active)
    return standby


def build_use_tracking_tree(DC, AZ, SV, Ad, Adz, Adzs, L, RN):
    used_tree = dict()
    used_tree['type'] = 'root node'
    used_tree['name'] = 'root'
    used_tree['child_nodes'] = []
    used_tree['left_server_num'] = sum([len(SV[d, z]) for d in DC for z in AZ[d]])
    for d in DC:
        node = dict()
        used_tree['type'] = 'center'
        node['name'] = d
        node['parent_node'] = used_tree
        node['child_nodes'] = []
        node['used_child_num'] = 0
        node['latency'] = {}
        for d_ in DC:
            node['latency'][RN[d_]] = L[d, RN[d_]]
        used_tree['child_nodes'].append(node)
    for dc in used_tree['child_nodes']:
        for z in AZ[dc['name']]:
            node = dict()
            node['type'] = 'zone'
            node['name'] = z
            node['parent_node'] = dc
            node['child_nodes'] = []
            node['used_child_num'] = 0
            dc['child_nodes'].append(node)
    for dc in used_tree['child_nodes']:
        for az in dc['child_nodes']:
            for s in SV[dc['name'], az['name']]:
                node = dict()
                node['type'] = 'server'
                node['name'] = s
                node['parent_node'] = az
                node['child_nodes'] = None
                node['availability'] = Ad[dc['name']] * Adz[dc['name'], az['name']] * Adzs[dc['name'], az['name'], s]
                az['child_nodes'].append(node)
    return used_tree
