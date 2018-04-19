# Constants
N_DC = 10
N_RN = 10
L_max = 200
Af = 0.99

# mapping title to data
TITLE_DATA_MAP = {
    'Average availability': 'aver_avail',
    'Total number of standbys': 'num_stb_total',
    'Total bandwidth usage': 'total_bw'
}

# mapping title and y limit
TITLE_YLIMIT_MAP = {
    'Average availability': (0.99, 1),
    'Total number of standbys': (0, 50),
    'Total bandwidth usage': (2000, 7000)
}
