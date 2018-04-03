import json


def cal_avail(tree):
    temp = 1
    # calculate availability recursively
    for x in tree.keys():
        if tree[x]['n_node']:
            temp = temp*(1 - tree[x]['av']*cal_avail(tree[x]['n_node']))
            print(temp)
        else:
            return tree[x]['av']

    return 1 - temp


def add_node(d, z, s, av_tree):
    if d not in av_tree:
        av_tree[d] = {}
        av_tree[d]['av'] = 0.99
        av_tree[d]['n_node'] = {}
    if z not in av_tree[d]['n_node']:
        av_tree[d]['n_node'][z] = {}
        av_tree[d]['n_node'][z]['av'] = 0.95
        av_tree[d]['n_node'][z]['n_node'] = {}
    if s not in av_tree[d]['n_node'][z]['n_node']:
        av_tree[d]['n_node'][z]['n_node'][s] = {}
        av_tree[d]['n_node'][z]['n_node'][s]['av'] = 0.9
        av_tree[d]['n_node'][z]['n_node'][s]['n_node'] = {}
    if 'func' not in av_tree[d]['n_node'][z]['n_node'][s]['n_node']:
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func'] = {}
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func']['av'] = 0.9
        av_tree[d]['n_node'][z]['n_node'][s]['n_node']['func']['n_node'] = None


if __name__ == '__main__':
    x ="test"
    print("can't place for active at %s" %x)

