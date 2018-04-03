from constants import *


def cal_avail(tree):
    temp = 1
    # calculate availability recursively
    for x in tree.keys():
        if tree[x]['subtree']:
            temp = temp*(1 - tree[x]['av']*cal_avail(tree[x]['subtree']))
            print(temp)
        else:
            return tree[x]['av']
    return 1 - temp


def add_node(d, z, s, av_tree, a_d, a_z, a_s):
    if d not in av_tree:
        av_tree[d] = {}
        av_tree[d]['av'] = a_d
        av_tree[d]['subtree'] = {}
    if z not in av_tree[d]['subtree']:
        av_tree[d]['subtree'][z] = {}
        av_tree[d]['subtree'][z]['av'] = a_z
        av_tree[d]['subtree'][z]['subtree'] = {}
    if s not in av_tree[d]['subtree'][z]['subtree']:
        av_tree[d]['subtree'][z]['subtree'][s] = {}
        av_tree[d]['subtree'][z]['subtree'][s]['av'] = a_s
        av_tree[d]['subtree'][z]['subtree'][s]['subtree'] = {}
    if 'func' not in av_tree[d]['subtree'][z]['subtree'][s]['subtree']:
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func'] = {}
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func']['av'] = Af
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func']['subtree'] = None