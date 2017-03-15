

def run_load_left_to_right(axle_spacing, axle_wt,
        span_length1, span_length2, num_nodes, space_to_trailing_load, distributed_load):
    V_max1 = []
    V_min1 = []
    M_max1 = []
    V_max2 = []
    V_min2 = []
    M_max2 = []

    total_span_length = span_length1 + span_length2

    dx = total_span_length/(num_nodes - 1) #the first node is x = 0
    x = 0
    add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
        distributed_load, total_span_length)
    #makes updating the location of the axle easier
    axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    abs_axle_location = get_abs_axle_location(axle_spacing)
    num_axles = len(axle_wt)
    axle_num = get_axle_num(num_axles)

    while x <= total_span_length:
        Vmax1 = 0.0
        Vmin1 = 0.0
        Mmax1 = 0.0
        Vmax2 = 0.0
        Vmin2 = 0.0
        Mmax2 = 0.0
        Rmax_pier = 0.0
        prev_axle_loc = []
        for axle_id in axle_num:
            #calc current location of all axles on span with the axle_id axle over the current node
            cur_axle_loc = move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc, num_axles)

            prev_axle_loc = cur_axle_loc

            Pt1, xt1, Pl1, xl1, Pr1, xr1 = calc_load_and_loc(cur_axle_loc,
                    axle_wt, x, 0.0, span_length1, num_axles)

            Pt2, xt2, Pl2, xl2, Pr2, xr2 = calc_load_and_loc(cur_axle_loc,
                    axle_wt, x, span_length1, span_length2, num_axles)

            Rb1, Re1 = calc_reactions(Pt1, xt1, span_length1) 

            Rb2, Re2 = calc_reactions(Pt2, xt2, span_length2)

            Rpier = calc_pier_reaction(Pt1, xt1, Pt2, xt2, span_length1,
                    span_length2)

            envelope_pier_reaction(Rmax_pier, Rpier)

            Vb1, Ve1 = calc_shear(Rb1, Re2, Pr1, Pl1)

            Vb2, Ve2 = calc_shear(Rb2, Re2, Pr2, Pl2)

            envelope_shear(Vmax1, Vmin1, Vb1, Ve1)

            envelope_shear(Vmax2, Vmin2, Vb2, Ve2)

            M1 = calc_moment(x, xl1, Rb1, Pl1)

            M2 = calc_moment(x, xl2, Rb2, Pl2)

            envelope_moment(Mmax1, M1)

            envelope_moment(Mmax2, M2)

        x = x + dx

        V_max1.append(Vmax1)
        V_min1.append(Vmin1)
        M_max1.append(Mmax1)

        V_max2.append(Vmax2)
        V_min2.append(Vmin2)
        M_max2.append(Mmax2)

    output(V_max1, V_min1, M_max1, V_max2, V_min2, M_max2)

def output(V_max1, V_min1, M_max1, V_max2, V_min2, M_max2):
    print max(V_max1)/2
    print min(V_min1)/2
    print max(M_max1)/2
    
def calc_reactions(Pt, xt, span_length):
    """Calculate reactions."""
    if span_length == 0.0:
        Rb = 0.0
        Re = 0.0
    else:
        Rb = Pt*(span_length-xt)/span_length
        Re = Pt*(span_length - xt)/span_length

    return Rb, Re

def calc_pier_reaction(Pt1, xt1, Pt2, xt2, span_length1, span_length2):
    if span_length2 == 0.0:
        Rpier = 0.0
    else:
        Rpier = Pt1*(xt1/span_length1) + Pt2*(span_length2 - xt2)/span_length2

    return Rpier

def envelope_pier_reaction(Rmax_pier, Rpier):
    if Rpier > Rmax_pier:
        Rmax_pier = Rpier

def calc_shear(Ra, Rb, Pr, Pl):
    """Calculate shear on each side of the node."""
    Vac = Rb - Pr 
    Vbc = Pl - Ra

    return Vac, Vbc

def envelope_shear(Vmax, Vmin, Vac, Vbc):
    """Envelope the maximum and minimum shear at each node."""
    if Vac < 0:
        if Vac < Vmin:
            Vmin = Vac
    if Vac >= 0:
        if Vac > Vmax:
            Vmax = Vac 

    if Vbc < 0:
        if Vbc < Vmin:
            Vmin = Vbc
    if Vbc >= 0:
        if Vbc > Vmax:
            Vmax = Vbc

def calc_moment(x, xl, Ra, Pl):
    """Calculate moment at node."""
    e = x - xl 
    Mc = Ra*x - Pl*e

    return Mc

def envelope_moment(Mmax, Mc):
    """Envelope maximum positive moment at each node."""
    if Mc > Mmax:
        Mmax = Mc

def get_axle_num(num_axles):
    """Numbers the axles starting with 0."""
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num


def get_abs_axle_location(axle_spacing):
    """Calculates the absolute location of the axles, left support is the
    origin."""
    abs_axle_location = []

    loc = 0.00 #initialize

    for spacing in axle_spacing:
        loc = loc + spacing 
        abs_axle_location.append(loc)

    return abs_axle_location          

#updating the location of each axle             
def move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc, num_axles):
    """Steps the axles across the span placing each axle at each node (critical
    section."""
    cur_axle_loc = []
    
    for i in range(num_axles):
        if axle_id == 1 and i == 0:
            #sets the initial locaction of the first axle
            axle_loc = x
        elif axle_id == 1 and i > 0:
            #sets the intial location of all subsequent axles
            axle_loc = x - abs_axle_location[i]
        else:
            axle_loc = prev_axle_loc[i] + axle_spacing[axle_id-1] 

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
        distributed_load, total_span_length):
    """Approximates the distributed trailing load as closely spaced point
    loads."""

    #approximate a distributed trailing load as closely spaced point loads
    #each point load is the distributed load times the point load spacing
    #the point load spacing is a function of the span lenght and number of
    #divisions required
    

    pt_load_spacing = 0.5
    num_loads = int(total_span_length/pt_load_spacing)
    equivalent_pt_load = distributed_load*pt_load_spacing

    axle_spacing.append(space_to_trailing_load)
    axle_wt.append(equivalent_pt_load)

    for x in range(num_loads):
        axle_spacing.append(pt_load_spacing)
        axle_wt.append(equivalent_pt_load)

    
        
        
                
if __name__ == "__main__":
    #input
    axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load = 5.00
    distributed_load = 8.00
    #axle_spacing = []
    #axle_wt = [1.0]
    span_length1 = 20.0
    span_length2 = 0.0
    num_nodes = 21.0 #should always be odd to capture maximum moment at mid span

    run_load_left_to_right(axle_spacing, axle_wt,
        span_length1, span_length2, num_nodes, space_to_trailing_load, distributed_load)
    

'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
