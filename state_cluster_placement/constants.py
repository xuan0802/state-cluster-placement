# Constants
L_max = 200
Af = 0.99
RD_init = 10
RD_unit = 0.01
BWT_unit = 0.1
BWR_attach = 0.1
BWR_ses_req = 0.1


# mapping title to data
TITLE_DATA_MAP = {
    'Average availability': 'aver_avail',
    'Total number of standbys': 'num_stb_total',
    'Total bandwidth usage': 'total_bw'
}

# mapping title and y limit
TITLE_YLIMIT_MAP = {
    'Average availability': (0.998, 1),
    'Total number of standbys': (10, 150),
    'Total bandwidth usage': (8000, 35000)
}
