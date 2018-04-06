from state_cluster_placement.constants import *


def cal_avail(tree):
    temp = 1
    # calculate availability recursively
    for x in tree.keys():
        if tree[x]['n_node']:
            temp = temp*(1 - tree[x]['av']*cal_avail(tree[x]['n_node']))
        else:
            return tree[x]['av']
    return 1 - temp


def add_node(d, z, s, av_tree, a_d, a_z, a_s):
    if d not in av_tree:
        av_tree[d] = {}
        av_tree[d]['av'] = a_d
        av_tree[d]['n_node'] = {}
    if z not in av_tree[d]['n_node']:
        av_tree[d]['n_node'][z] = {}
        av_tree[d]['n_node'][z]['av'] = a_z
        av_tree[d]['n_node'][z]['n_node'] = {}
    if s not in av_tree[d]['n_node'][z]['n_node']:
        av_tree[d]['n_node'][z]['n_node'][s] = {}
        av_tree[d]['n_node'][z]['n_node'][s]['av'] = a_s
        av_tree[d]['n_node'][z]['n_node'][s]['n_node'] = {}
    if 'func' not in av_tree[d]['n_node'][z]['n_node'][s]['n_node']:
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func'] = {}
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func']['av'] = Af
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func']['n_node'] = None
