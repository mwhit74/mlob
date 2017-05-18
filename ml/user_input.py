def get_input():
    """Get user inputs for calculation values."""
    axle_spacing = get_axle_spacing()
    axle_wt = get_axle_wt()
    space_to_trailing_load = get_space_to_trailing_load()
    distributed_load = get_distributed_load()
    span1_length = get_span1_length()
    span2_length = get_span2_length()
    num_analysis_nodes = get_num_analysis_nodes()

def get_axle_spacing():
    """Get axle spacing from user"""
    print "Enter axle spacing values separated by a space. Hit enter when done."
    while True:
        try:
            axle_spacing=([float(x) for x in raw_input().split(' ')])
        except ValueError:
            print """Invalid values. Please only enter numbers.\n
                     Start from beginning of axle spacing values:"""
        else:
            break

    return axle_spacing

def get_axle_wt():
    """Get axle weights from user"""
    print "Enter axle weight values separated by a space. Hit enter when done."
    while True:
        try:
            axle_wt=([float(x) for x in raw_input().split(' ')])
            if len(axle_wt) != (len(axle_spacing) + 1):
                print "Please enter %d axle weight values:" % (len(axle_spacing) + 1)
                continue
        except ValueError:
            print """Invalid values. Please only enter numbers.\n
                     Start from beginning of axle weight values:"""
        else:
            break

    return axle_wt

def get_space_to_trailing_load():
    """Get space to trailing load from user"""
    print "Enter value of the space to trailing load. Hit enter when done."
    while True:
        try:
            space_to_trailing_load=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break
    
    return space_to_trailing_load

def get_distributed_load():
    """Get distributed trailing load from user"""
    print "Enter value of the distributed load. Hit enter when done."
    while True:
        try:
            distributed_load=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    return distributed_load

def get_span1_length():
    """Get span 1 length from user"""
    print "Enter value of span length 1. Hit enter when done."
    while True:
        try:
            span1_length=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    return span1_length

def get_span2_length():
    """Get span 2 length from user"""
    print "Enter value of span length 2. Hit enter when done."
    while True:
        try:
            span2_length=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    return span2_length

def get_num_analysis_nodes():
    """Get number of analysis nodes from user"""
    print """Enter the number of nodes as an integer. \
             Number should be odd and greater than or equal to 21."""
    while True:
        try:
            num_nodes=(int(raw_input()))
            if num_nodes < 21:
                print """Number of nodes should be greater than or equal to 21\n
                         Please enter the number of nodes:"""
                continue
            elif (num_nodes % 2) == 0:
                print "Please enter an odd number of nodes:"
                continue
        except ValueError:
            print "Invalid value. Please enter an integer:"
        else:
            break

    return num_nodes


