
def print_placement(placement):
    """print placement nicely"""
    placement.sort(key=lambda x: x['act'])
    for p in placement:
        print(p)

