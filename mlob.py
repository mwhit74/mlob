import pdb
import timeit

def analyze_vehicle(axle_spacing, axle_wt, span_length1, span_length2,
                    num_nodes, space_to_trailing_load,
                    distributed_load):
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

        if direction == "ltr":
            start_pt = span1_begin
        elif direction == "rtl":
            start_pt = span2_end
        abs_axle_location = get_abs_axle_location(axle_spacing, start_pt)

        for x in node_loc: 
            Vmax1 = 0.0
            Vmin1 = 0.0
            Mmax1 = 0.0
            Vmax2 = 0.0
            Vmin2 = 0.0
            Mmax2 = 0.0
            Rmax_pier = 0.0
            prev_axle_loc = []
        
            #print "x: " + str(x)
            for axle_id in axle_num:
                #print "axle_id: " + str(axle_id)
                cur_axle_loc = move_axle_loc(x, axle_spacing,
                                             abs_axle_location, axle_id,
                                             prev_axle_loc, num_axles, direction)
                prev_axle_loc = cur_axle_loc
                #print cur_axle_loc
        
                Pt1, xt1, Pl1, xl1, Pr1, xr1 = calc_load_and_loc(cur_axle_loc,
                           axle_wt, x, span1_begin, span1_end, num_axles)
                   
                Pt2, xt2, Pl2, xl2, Pr2, xr2 = calc_load_and_loc(cur_axle_loc,
                        axle_wt, x, span2_begin, span2_end, num_axles)
                
                Rpier = calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin,
                                           span1_end, span2_begin, span2_end)
                
                Rmax_pier = envelope_pier_reaction(Rmax_pier, Rpier)
                
        
        
                if x >= span1_begin and x <= span1_end:
        
                    Rb1, Re1 = calc_reactions(Pt1, xt1, span1_begin, span1_end) 
                    
                    Vb1, Ve1 = calc_shear(Rb1, Re1, Pr1, Pl1)
                    
                    Vmax1, Vmin1 = envelope_shear(Vmax1, Vmin1, Vb1, Ve1)
                    
                    M1 = calc_moment(x, xl1, span1_begin, Rb1, Pl1)
                    
                    Mmax1 = envelope_moment(Mmax1, M1)
        
                    V_max1.append(Vmax1)
                    V_min1.append(Vmin1)
                    M_max1.append(Mmax1)
                    
        
        
                if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
        
                    Rb2, Re2 = calc_reactions(Pt2, xt2, span2_begin, span2_end)
        
                    Vb2, Ve2 = calc_shear(Rb2, Re2, Pr2, Pl2)
        
                    Vmax2, Vmin2 = envelope_shear(Vmax2, Vmin2, Vb2, Ve2)
        
                    M2 = calc_moment(x, xl2, span2_begin, Rb2, Pl2)
        
                    Mmax2 = envelope_moment(Mmax2, M2)
        
                    V_max2.append(Vmax2)
                    V_min2.append(Vmin2)
                    M_max2.append(Mmax2)
                    
        
                    #print "Pt2: " + str(Pt2)
                    #print "xt2: " + str(xt2)
                    #print "Pl2: " + str(Pl2)
                    #print "xl2: " + str(xl2)
                    #print "Pr2: " + str(Pr2)
                    #print "xr2: " + str(xr2)
                    #print "Rb2: " + str(Rb2)
                    #print "Re2: " + str(Re2)
                    #print "Vb2: " + str(Vb2)
                    #print "Ve2: " + str(Ve2)
                    #print "Vmax2: " + str(Vmax2)
                    #print "Vmin2: " + str(Vmin2)
                    #print "M2: " + str(M2)
                    
                """
                #print Pt1, xt1, Pl1, xl1, Pr1, xr1
                #print Rb1, Re1
                #print Vb1, Ve1
                #print Vmax1, Vmin1
                """
                
                
                #stop = raw_input(">")
                
    
    
    output(V_max1, V_min1, M_max1, V_max2, V_min2, M_max2, Rmax_pier)

def output(V_max1, V_min1, M_max1, V_max2, V_min2, M_max2, Rmax_pier):
    """Format and print output."""
    print max(V_max1)/2
    print min(V_min1)/2
    print max(M_max1)/2

    if V_max2 != []:
        print max(V_max2)/2
        print min(V_min2)/2
        print max(M_max2)/2
        
    print Rmax_pier/2
    
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
        Rpier = Pt1*(xt1 - span1_begin)/span_length1 + Pt2*(span2_end - xt2)/span_length2

    return Rpier

def envelope_pier_reaction(Rmax_pier, Rpier):
    """Envelope the maximum interior pier (floorbeam) reaction."""
    if Rpier > Rmax_pier:
        Rmax_pier = Rpier

    return Rmax_pier

def calc_shear(Rb, Re, Pr, Pl):
    """Calculate shear on each side of the node."""
    Vb = Re - Pr 
    Ve = Pl - Rb

    return Vb, Ve

def envelope_shear(Vmax, Vmin, Vb, Ve):
    """Envelope the maximum and minimum shear at each node."""
    if Vb < 0:
        if Vb < Vmin:
            Vmin = Vb
    if Vb >= 0:
        if Vb > Vmax:
            Vmax = Vb 

    if Ve < 0:
        if Ve < Vmin:
            Vmin = Ve
    if Ve >= 0:
        if Ve > Vmax:
            Vmax = Ve

    return Vmax, Vmin

def calc_moment(x, xl, span_begin, Rb, Pl):
    """Calculate moment at node."""
    el = x - xl 
    eb = x - span_begin
    M = Rb*eb- Pl*el

    return M

def envelope_moment(Mmax, M):
    """Envelope maximum positive moment at each node."""
    if M > Mmax:
        Mmax = M

    return Mmax

def get_axle_num(num_axles):
    """Numbers the axles starting with 0."""
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num


def get_abs_axle_location(axle_spacing, start_pt):
    """Calculates the absolute location of the axles, left support is the
    origin."""
    abs_axle_location = []

    loc = start_pt #initialize

    for spacing in axle_spacing:
        loc = loc + spacing 
        abs_axle_location.append(loc)

    return abs_axle_location          

def move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc,
                  num_axles, direction):
    """Steps the axles across the span placing each axle at each node."""
    #calc current location of all axles on span with the
    #axle_id axle over the current node

    cur_axle_loc = []
    
    for i in range(num_axles):
        if axle_id == 1 and i == 0:
            #sets the initial locaction of the first axle
            axle_loc = x
        elif axle_id == 1 and i > 0 and direction == "ltr":
            #sets the intial location of all subsequent axles for moving left to
            #right
            axle_loc = x - abs_axle_location[i]
        elif axle_id == 1 and i > 0 and direction == "rtl":
            #sets the intial location of all subsequent axles for moving right
            #to left
            axle_loc = x + abs_axle_location[i]
        elif axle_id > 1 and direction == "ltr":
            axle_loc = prev_axle_loc[i] + axle_spacing[axle_id-1] 
        elif axle_id > 1 and direction == "rtl":
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
        
                
if __name__ == "__main__":
    start = timeit.default_timer()
    #input
    axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load = 5.00
    distributed_load = 8.00
    #axle_spacing = []
    #axle_wt = [1.0]
    span_length1 = 189.0
    span_length2 = 189.0
    """
    num_nodes should always be odd to place a node at midspan and at 
    each support
    a minimum of 3 nodes should be used for analysis
    """
    num_nodes = 21

    analyze_vehicle(axle_spacing, axle_wt, span_length1, span_length2, num_nodes,
                    space_to_trailing_load, distributed_load)

    stop = timeit.default_timer()
    print stop - start
    

'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
