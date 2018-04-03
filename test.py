import json


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


def add_node(d, z, s, av_tree):
    if d not in av_tree:
        av_tree[d] = {}
        av_tree[d]['av'] = 0.99
        av_tree[d]['subtree'] = {}
    if z not in av_tree[d]['subtree']:
        av_tree[d]['subtree'][z] = {}
        av_tree[d]['subtree'][z]['av'] = 0.95
        av_tree[d]['subtree'][z]['subtree'] = {}
    if s not in av_tree[d]['subtree'][z]['subtree']:
        av_tree[d]['subtree'][z]['subtree'][s] = {}
        av_tree[d]['subtree'][z]['subtree'][s]['av'] = 0.9
        av_tree[d]['subtree'][z]['subtree'][s]['subtree'] = {}
    if 'func' not in av_tree[d]['subtree'][z]['subtree'][s]['subtree']:
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func'] = {}
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func']['av'] = 0.9
        av_tree[d]['subtree'][z]['subtree'][s]['subtree']['func']['subtree'] = None


if __name__ == '__main__':
    av_tree = {}
    d = 'dc1'
    z = 'az1'
    s = 'sv1'
    add_node(d, z, s, av_tree)
    print(json.dumps(av_tree, indent=2))
    print(cal_avail(av_tree))


