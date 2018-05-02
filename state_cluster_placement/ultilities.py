import ujson
from ast import literal_eval
import numpy as np
from matplotlib import pyplot as plt
from state_cluster_placement.constants import *


def print_placement(placement):
    """print placement nicely"""
    placement.sort(key=lambda x: x['act'])
    for p in placement:
        print(p)


def save_to_file(input_dict, filename):
    """save topo to a json file"""
    f = open(filename, "w")
    ujson.dump(input_dict, f)
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
    input['Ad'] = Ad
    input['Adz'] = Adz
    input['Adzs'] = Adzs

    return input


def draw_bar_chart(xtick, title, *algorithms):
    """draw a bar chart"""
    fig, ax = plt.subplots()
    color_list = ['blue', 'red', 'green', 'black', 'yellow']
    index = np.arange(len(xtick))
    bar_width = 0.2
    opacity = 0.8
    i = 0
    for algo in algorithms:
        ax.bar(index + i * bar_width, algo[TITLE_DATA_MAP[title]],
               bar_width, alpha=opacity, color=color_list[i], label=algo['label'])
        i = i + 1
    ax.set_ylim(TITLE_YLIMIT_MAP[title])
    ax.set_xlabel('A_min', fontsize='x-large')
    ax.set_ylabel(title, fontsize='x-large')
    ax.set_xticks(index + bar_width)
    ax.set_xticklabels(xtick)
    ax.legend(fontsize='large')
    fig.tight_layout()
    plt.show()
