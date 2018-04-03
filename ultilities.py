
def print_placement(result):
    """print placement nicely"""
    result_ = result.keys()
    result_.sort(key=lambda x: x[0][0])
    for r in result_:
        print(r)

