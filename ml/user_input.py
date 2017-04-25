def get_input():
    """Get user inputs for calculation values."""
    print "Enter axle spacing values separated by a space. Hit enter when done."
    while True:
        try:
            axle_spacing=([float(x) for x in raw_input().split(' ')])
        except ValueError:
            print """Invalid values. Please only enter numbers.\n
                     Start from beginning of axle spacing values:"""
        else:
            break

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

    print "Enter value of the space to trailing load. Hit enter when done."
    while True:
        try:
            space_to_trailing_load=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    print "Enter value of the distributed load. Hit enter when done."
    while True:
        try:
            distributed_load=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    print "Enter value of span length 1. Hit enter when done."
    while True:
        try:
            span_length1=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

    print "Enter value of span length 2. Hit enter when done."
    while True:
        try:
            span_length2=(float(raw_input()))
        except ValueError:
            print "Invalid value. Please enter one number."
        else:
            break

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

    return axle_spacing, axle_wt, space_to_trailing_load, distributed_load, \
           span_length1, span_length2, num_nodes


