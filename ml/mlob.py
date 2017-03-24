import pdb
import timeit

def analyze_vehicle(axle_spacing, axle_wt, span_length1, span_length2,
                    num_nodes, space_to_trailing_load,
                    distributed_load):
    """Initialize variables, set up loops, run analysis by calling functions."""
    #calculates for a full track (2 rails)
    V_max1 = []
    V_min1 = []
    M_max1 = []
    V_max2 = []
    V_min2 = []
    M_max2 = []

    span1_begin = 0.0
    span1_end = span_length1
    span2_begin = span_length1
    span2_end = span_length1 + span_length2

    node_loc_ltr = node_location(span1_begin, span1_end, span2_begin,
                                 span2_end, num_nodes)
    node_loc_rtl = list(reversed(node_loc_ltr))

    add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
                      distributed_load, span1_begin, span2_end)
    axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    num_axles = len(axle_wt)
    axle_num = get_axle_num(num_axles)
    
    for node_loc,direction in zip([node_loc_ltr, node_loc_rtl], ["ltr", "rtl"]):
        
        for x,i in zip(node_loc, range(len(node_loc))): 
            #pdb.set_trace()
            Vmax1 = 0.0
            Vmin1 = 0.0
            Mmax1 = 0.0
            Vmax2 = 0.0
            Vmin2 = 0.0
            Mmax2 = 0.0
            Rmax_pier = 0.0
        
            for axle_id in axle_num:
                if axle_id == 1:
                    cur_axle_loc = get_abs_axle_location(axle_spacing, x,
                            direction)
                else:
                    prev_axle_loc = cur_axle_loc

                    cur_axle_loc = move_axle_loc(x, axle_spacing, axle_id,
                                                 prev_axle_loc, num_axles,
                                                 direction)

                Pt1, xt1, Pl1, xl1, Pr1, xr1 = calc_load_and_loc(cur_axle_loc,
                           axle_wt, x, span1_begin, span1_end, num_axles)
                   
                Pt2, xt2, Pl2, xl2, Pr2, xr2 = calc_load_and_loc(cur_axle_loc,
                        axle_wt, x, span2_begin, span2_end, num_axles)
                
                Rpier = calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin,
                                           span1_end, span2_begin, span2_end)
                
                Rmax_pier = envelope_pier_reaction(Rmax_pier, Rpier)
                
                if x >= span1_begin and x <= span1_end:
        
                    Rb1, Re1 = calc_reactions(Pt1, xt1, span1_begin, span1_end) 
                    
                    Vb1, Ve1 = calc_shear(Rb1, Re1, Pr1, Pl1, direction)
                    
                    Vmax1 = envelope_max_shear(Vb1, Ve1, V_max1, i)

                    Vmin1 = envelope_min_shear(Vb1, Ve1, V_min1, i)
                    
                    M1 = calc_moment(x, xl1, span1_begin, Rb1, Pl1)
                    
                    Mmax1 = envelope_moment(M1, M_max1, i)
        
                if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
        
                    Rb2, Re2 = calc_reactions(Pt2, xt2, span2_begin, span2_end)
        
                    Vb2, Ve2 = calc_shear(Rb2, Re2, Pr2, Pl2, direction)

                    Vmax2 = envelope_max_shear(Vb2, Ve2, V_max2, i)

                    Vmin2 = envelope_min_shear(Vb2, Ve2, V_min2, i)
        
                    M2 = calc_moment(x, xl2, span2_begin, Rb2, Pl2)
        
                    Mmax2 = envelope_moment(M2, M_max2, i)

    return node_loc_ltr, V_max1, V_min1, M_max1, V_max2, V_min2, M_max2, \
           Rmax_pier, span1_begin, span2_begin
    
def calc_reactions(Pt, xt, span_begin, span_end):
    """Calculate reactions."""
    span_length = span_end - span_begin
    if span_length == 0.0:
        Rb = 0.0
        Re = 0.0
    else:
        Rb = Pt*(span_end - xt)/span_length
        Re = Pt*(xt - span_begin)/span_length

    return Rb, Re

def calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin, span1_end, span2_begin,
        span2_end):
    """Calculate the interior pier (floorbeam) reaction."""
    span_length1 = span1_end - span1_begin
    span_length2 = span2_end - span2_begin
    if span_length2 == 0.0:
        Rpier = 0.0
    else:
        Rpier = (Pt1*(xt1 - span1_begin)/span_length1 +
                    Pt2*(span2_end - xt2)/span_length2)

    return Rpier

def envelope_pier_reaction(Rmax_pier, Rpier):
    """Envelope the maximum interior pier (floorbeam) reaction."""
    if Rpier > Rmax_pier:
        Rmax_pier = Rpier

    return Rmax_pier

def calc_shear(Rb, Re, Pr, Pl, direction):
    """Calculate shear on each side of the node."""
    if direction == "ltr":
        Vb = Re - Pr
        Ve = Pl - Rb
    elif direction == "rtl":
        #Vb = Re - Pr
        #Ve = Pl - Rb
        Vb = 0
        Ve = 0

    return Vb, Ve

def envelope_max_shear(Vb, Ve, V_max, i):
    """Envelope the maximum and minimum shear at each node."""
    Vmax = max(Vb, Ve) 

    try:
        if V_max[i] < Vmax:
            V_max[i] = Vmax
    except:
        V_max.append(Vmax)

def envelope_min_shear(Vb, Ve, V_min, i):
    """Envelope the maximum and minimum shear at each node."""
    Vmin = min(Vb, Ve)

    try:
        if V_min[i] > Vmin:
            V_min[i] = Vmin
    except:
        V_min.append(Vmin)

def calc_moment(x, xl, span_begin, Rb, Pl):
    """Calculate moment at node."""
    el = x - xl 
    eb = x - span_begin
    M = Rb*eb- Pl*el

    return M

def envelope_moment(M, M_max, i):
    """Envelope maximum positive moment at each node."""
    try:
        if M_max[i] < M:
            M_max[i] = M
    except:
        M_max.append(M)

def get_axle_num(num_axles):
    """Numbers the axles starting with 0."""
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num


def get_abs_axle_location(axle_spacing, start_pt, direction):
    """Calculates the absolute location of the axles, left support is the
    origin."""
    abs_axle_location = []

    loc = start_pt #initialize

    for spacing in axle_spacing:
        if direction == "ltr":
            loc = loc - spacing
        elif direction == "rtl":
            loc = loc + spacing 
        abs_axle_location.append(loc)

    return abs_axle_location          

def move_axle_loc(x, axle_spacing, axle_id, prev_axle_loc,
                  num_axles, direction):
    """Steps the axles across the span placing each axle at each node."""
    #calc current location of all axles on span with the
    #axle_id axle over the current node

    cur_axle_loc = []
    
    for i in range(num_axles):
        if direction == "ltr":
            axle_loc = prev_axle_loc[i] + axle_spacing[axle_id-1] 
        elif direction == "rtl":
            axle_loc = prev_axle_loc[i] - axle_spacing[axle_id-1]

        cur_axle_loc.append(axle_loc)

    return cur_axle_loc
    
def calc_load_and_loc(cur_axle_loc, axle_wt, x, begin_span, end_span, num_axles):
    """Calculates the total load and its location on the span, and the load and
    its location to the left and right of the node (critical section)."""

    Pt = 0.0
    xt = 0.0
    sum_Ptx = 0.0

    Pl = 0.0
    xl = 0.0
    sum_Plx = 0.0

    Pr = 0.0
    xr = 0.0
    sum_Prx = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= begin_span and cur_axle_loc[i] <= end_span:
            Pt = Pt + axle_wt[i]
            sum_Ptx = sum_Ptx + cur_axle_loc[i]*axle_wt[i]

            if cur_axle_loc[i] >= begin_span and cur_axle_loc[i] <= x:
                Pl = Pl + axle_wt[i]
                sum_Plx = sum_Plx + cur_axle_loc[i]*axle_wt[i]
            
            if cur_axle_loc[i] >= x and cur_axle_loc[i] <= end_span:
                Pr = Pr + axle_wt[i]
                sum_Prx = sum_Prx + cur_axle_loc[i]*axle_wt[i]
            
    #avoid divide by zero error
    if Pt == 0:
        xt = 0
    else:        
        xt = sum_Ptx/Pt

    if Pl == 0:
        xl = 0
    else:        
        xl = sum_Plx/Pl

    if Pr == 0:
        xr = 0
    else:        
        xr = sum_Prx/Pr

    return Pt, xt, Pl, xl, Pr, xr
    
def add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
        distributed_load, span1_begin, span2_end):
    """Approximates the distributed trailing load as closely spaced point
    loads."""

    #approximate a distributed trailing load as closely spaced point loads
    #each point load is the distributed load times the point load spacing
    #the point load spacing is a function of the span lenght and number of
    #divisions required
    
    total_span_length = span2_end - span1_begin
    pt_load_spacing = 0.5
    num_loads = int(total_span_length/pt_load_spacing)
    equivalent_pt_load = distributed_load*pt_load_spacing

    axle_spacing.append(space_to_trailing_load)
    axle_wt.append(equivalent_pt_load)

    for x in range(num_loads):
        axle_spacing.append(pt_load_spacing)
        axle_wt.append(equivalent_pt_load)

def node_location(span1_begin, span1_end, span2_begin, span2_end, num_nodes):

    span_length1 = span1_end - span1_begin
    span_length2 = span2_end - span2_begin

    node_loc = []
    x1 = 0.0
    dx1 = span_length1/(num_nodes - 1)

    for i in range(num_nodes):
        if i == 0:
            node_loc.append(x1)
        else:
            x1 = x1 + dx1
            node_loc.append(x1)

    if span_length2 > 0:

        x2 = span_length1
        dx2 = span_length2/(num_nodes - 1)
        
        for i in range(num_nodes):
            if i == 0:
                pass #second span beginning is end of first span
            else:
                x2 = x2 + dx2
                node_loc.append(x2)

    return node_loc


def get_inputs():
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

def output(axle_spacing, axle_wt, span_length1, span_length2, num_nodes,
            space_to_trailing_load, distributed_load, node_loc, V_max1,
            V_min1, M_max1, V_max2, V_min2, M_max2, Rmax_pier, analysis_time,
            span1_begin, span2_begin):
    """Format and print output."""
    #currently outputs half track (one rail)
    echo_input = ""
    out_tb = ""
    out_val = ""

    echo_input += "\n\nECHO INPUT\n"
    echo_input += "Axle spacing: " + str(axle_spacing) + "\n"
    echo_input += "Axle weights: " + str(axle_wt) + "\n"
    echo_input += "Length Span 1: " + str(span_length1) + "\n"
    echo_input += "Length Span 2: " + str(span_length2) + "\n"
    echo_input += "Number of Nodes: " + str(num_nodes) + "\n"
    echo_input += "Space to trailing load: " + str(space_to_trailing_load) + "\n"
    echo_input += "Distributed trailing load: " + str(distributed_load) + "\n"


    out_tb += "\n\nOUTPUT\n"
    out_tb += "SPAN 1"
    out_tb += "\n" #span 1 title spacing
    out_tb += "{0:^15s}{1:^15s}{2:^15s}".format("x [ft]",
                                                "Vmax [kip]",
                                                "Mmax [kip-ft]")
    out_tb += "\n" #span 1 header spacing

    for x,Vmax,Vmin,Mmax in zip(node_loc, V_max1, V_min1, M_max1):
        out_tb += """{0:^-15.3f}{1:^-15.3f}{2:^-15.3f}\n""".format(x,
                                                                   Vmax/2,
                                                                   Mmax/2)

    out_tb += "\n" #span 1 table spacing


    out_val += """Vmax [kip]: {0:<-.3f}\nMmax [kip-ft]: {1:<-.3f}""".format(max(V_max1)/2,
                                                                            max(M_max1)/2)
    out_val += "\n" #span 1 max/min spacing


    if V_max2 != []:
        out_tb += "SPAN 2"
        out_tb += "\n" #span 2 title spacing
        out_tb += "{0:^15s}{1:^15s}{2:^15s}".format("x [ft]",
                                                    "Vmax [kip]",
                                                    "Mmax [kip-ft]")
        out_tb += "\n" #span 2 header spacing

        for x,Vmax,Vmin,Mmax in zip(node_loc, V_max2, V_min2, M_max2):
            out_tb += """{0:^-15.3f}{1:^-15.3f}{2:^-15.3f}\n""".format(x,
                                                                       Vmax/2,
                                                                       Mmax/2)

        out_tb += "\n\n" #span 2 table spacing
        
        out_val += """Vmax [kip]: {0:<-.3f}\nMmax [kip-ft]: {1:<-.3f}""".format(max(V_max2)/2,
                                                                                max(M_max2)/2)

        out_val += "\nRmax_pier: {0:<-.3f}".format(Rmax_pier/2)
      
    print echo_input + out_tb + out_val
       
    print "Runtime [sec]: {0:<.3f}\n\n".format(analysis_time)

def manager():

     
    #input
    axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load = 0.00
    distributed_load = 0.00
    #axle_spacing = []
    #axle_wt = [1.0]
    span_length1 = 90.0
    span_length2 = 0.0
    #num_nodes should always be odd to place a node at midspan and at 
    #each support
    #a minimum of 21 nodes should be used for analysis
    num_nodes = 21 
     

    #axle_spacing, axle_wt, space_to_trailing_load, distributed_load, \
    #span_length1, span_length2, num_nodes = get_inputs()

    uias = [] #user_input_axle_spacing
    [uias.append(x) for x in axle_spacing]
    uiaw = [] #user_input_axle_wt
    [uiaw.append(x) for x in axle_wt]

    start = timeit.default_timer()

    node_loc, V_max1, V_min1, M_max1, V_max2, V_min2, M_max2, Rmax_pier,\
    span1_begin, span2_begin = analyze_vehicle(axle_spacing, axle_wt,
                                               span_length1, span_length2,
                                               num_nodes,
                                               space_to_trailing_load, 
                                               distributed_load)

    stop = timeit.default_timer()

    analysis_time = stop - start

    output(uias, uiaw, span_length1, span_length2, num_nodes,
            space_to_trailing_load, distributed_load, node_loc, V_max1,
            V_min1, M_max1, V_max2, V_min2, M_max2, Rmax_pier, analysis_time,
            span1_begin, span2_begin)

if __name__ == "__main__":

    manager()

