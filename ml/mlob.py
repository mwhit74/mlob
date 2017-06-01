from tqdm import tqdm

def analyze_vehicle(axle_spacing, axle_wt, span_length1, span_length2,
                     num_user_nodes, space_to_trailing_load, distributed_load,
                      point_load_spacing=0.5):
    """Initialize variables, set up loops, run analysis by calling functions."""
    #calculates for a full track (2 rails)
    V_max1 = []
    M_max1 = []
    V_max2 = []
    M_max2 = []

    (span1_begin,
    span1_end,
    span2_begin,
    span2_end) = span_begin_end_coords(span_length1, span_length2)

    node_loc_ltr = node_location(span1_begin, span1_end, span2_begin,
                                 span2_end, num_user_nodes)
    node_loc_rtl = list(reversed(node_loc_ltr))

    add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
                      distributed_load, span1_begin, span2_end,
                      point_load_spacing)
    axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    num_axles = len(axle_wt)
    axle_num = number_axles(num_axles)
    
    for node_loc,direction in tqdm(zip([node_loc_ltr, 
                                        node_loc_rtl],
                                        ["ltr","rtl"])):
        num_analysis_nodes = len(node_loc)

        #initialize span index id value
        if direction == "ltr":
            span1_index_id = -1
            span2_index_id = -1
        elif direction == "rtl":
            span1_index_id = num_user_nodes
            span2_index_id = num_user_nodes

        for x,i in tqdm(zip(node_loc, range(num_analysis_nodes))): 
            Ve1 = 0.0
            M1 = 0.0
            Ve2 = 0.0
            M2 = 0.0
            Rmax_pier = 0.0

            #calculate span index id value
            if x >= span1_begin and x <= span1_end:
                if direction == "ltr":
                    span1_index_id = span1_index_id + 1
                elif direction == "rtl":
                    span1_index_id = span1_index_id - 1

            if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
                if direction == "ltr":
                    span2_index_id = span2_index_id + 1
                elif direction == "rtl":
                    span2_index_id = span2_index_id - 1

            for axle_id in tqdm(axle_num):

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
                    Rb1, Re1 = calc_reactions(Pt1, xt1, span1_begin, span1_end, direction) 
                    
                    Ve1 = calc_shear(Rb1, Re1, Pr1, Pl1, direction)

                    envelope_shear(Ve1, V_max1, span1_index_id)

                    M1 = calc_moment(x, 
                                     xl1, 
                                     xr1, 
                                     span1_begin, 
                                     span1_end, 
                                     Rb1, 
                                     Pl1, 
                                     Pr1, 
                                     direction)
                    
                    envelope_moment(M1, M_max1, span1_index_id)
        
                if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
                    Rb2, Re2 = calc_reactions(Pt2, xt2, span2_begin, span2_end, direction)
        
                    Ve2 = calc_shear(Rb2, Re2, Pr2, Pl2, direction)

                    envelope_shear(Ve2, V_max2, span2_index_id)
        
                    M2 = calc_moment(x, 
                                     xl2, 
                                     xr2, 
                                     span2_begin, 
                                     span2_end, 
                                     Rb2, 
                                     Pl2, 
                                     Pr2, 
                                     direction)
        
                    envelope_moment(M2, M_max2, span2_index_id)


    return node_loc_ltr, V_max1, M_max1, V_max2, M_max2, \
           Rmax_pier, span1_begin, span2_begin
    
def calc_reactions(Pt, xt, span_begin, span_end, direction):
    """Calculate reactions.

    Calculates the reactions at the end of each span. The pier reaction is not
    calculated in this function.
    
    Moving left to right:
        Rb = Pt*(span_end - xt)/span_length
        Re = Pt*(xt - span_begin)/span_length
    Moving right to left:
        Rb = Pt*(xt - span_begin)/span_length
        Re = Pt*(span_end - xt)/span_length

    Args:
        Pt (float): total load on the span
        xt (float): location of the total load on the span
        span_begin (float): span begin coordinate
        span_end (float): span end coordinate
        direction (str): flag to determine which direction is being calculated,
                            either 'ltr' or 'rtl'
    """
    span_length = span_end - span_begin
    if span_length == 0.0:
        Rb = 0.0
        Re = 0.0
    else:
        if direction == "ltr":
            Rb = Pt*(span_end - xt)/span_length
            Re = Pt*(xt - span_begin)/span_length
        elif direction == "rtl":
            Rb = Pt*(xt - span_begin)/span_length
            Re = Pt*(span_end - xt)/span_length

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
    """Calculate shear on one side of the node."""
    #calculate shear on opposite side of section
    #if load move ltr, calc shear on right
    #if load move rtl, calc shear on left
    if direction == "ltr":
        Ve = Pl - Rb
    elif direction == "rtl":
        Ve = abs(Pr - Rb)

    return Ve

def envelope_shear(Ve, V_max, index_id):
    """Envelope the maximum and minimum shear at each node."""
    try:
        if V_max[index_id] < Ve:
            V_max[index_id] = Ve
    except:
        V_max.append(Ve)

def calc_moment(x, xl, xr, span_begin, span_end, Rb, Pl, Pr, direction):
    """Calculate moment at node."""
    if direction == "ltr":
        el = x - xl 
        eb = x - span_begin
        M = Rb*eb- Pl*el
    elif direction == "rtl":
        er = xr - x
        eb = span_end - x
        M = Rb*eb - Pr*er

    return M

def envelope_moment(M, M_max, index_id):
    """Envelope maximum positive moment at each node."""
    try:
        if M_max[index_id] < M:
            M_max[index_id] = M
    except:
        M_max.append(M)

def number_axles(num_axles):
    """Numbers the axles starting with 1."""
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
        distributed_load, span1_begin, span2_end, pt_load_spacing=0.5):
    """Approximates the distributed trailing load as closely spaced point
    loads."""

    #approximate a distributed trailing load as closely spaced point loads
    #each point load is the distributed load times the point load spacing
    #the point load spacing is a function of the span lenght and number of
    #divisions required
    if space_to_trailing_load < 0.0:
        raise ValueError("Must enter a positive float for space to trialing"
                            "load.")
    elif distributed_load < 0.0:
        raise ValueError("Must enter a positive float for distributed load.")
    elif pt_load_spacing <= 0.0:
        raise ValueError("Must enter a positive float (or nothing for default"
                            "value of 0.5) for the point load spacing.")
    elif distributed_load != 0.0 and space_to_trailing_load != 0.0:
        total_span_length = span2_end - span1_begin
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

    if span_length1 < 0.0:
        raise ValueError("Must enter a positive float for span 1 length.")
    elif span_length2 < 0.0:
        raise ValueError("Must enter a positive float for span 2 length (or"
                "nothing for a default value of 0.0).")
    elif num_nodes <= 0:
        raise ValueError("Must enter a postive interger for number of nodes"
                            "(the recommended minimum number of nodes is 21.).")
    else:
        node_loc = []
        
        #span length 1 node locations
        x1 = 0.0
        dx1 = span_length1/(num_nodes - 1)

        for i in range(num_nodes):
            if i == 0:
                node_loc.append(x1)
            else:
                x1 = x1 + dx1
                node_loc.append(x1)

        #span length 2 node locations
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

def span_begin_end_coords(span_length1, span_length2=0.0):
    """Calculate the span beginning and end coordinates for spans 1 and 2."""
    if span_length1 < 0.0:
        raise ValueError("Must enter a positive float for span 1 length.")
    elif span_length2 < 0.0:
        raise ValueError("Must enter a positive float for span 2 length (or"
                            "nothing for a default value of 0.0).")
    else:
        span1_begin = 0.0
        span1_end = span_length1
        span2_begin = span_length1
        span2_end = span_length1 + span_length2
        return span1_begin, span1_end, span2_begin, span2_end
