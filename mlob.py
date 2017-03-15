

def run_load_left_to_right(axle_spacing, axle_wt,
        span_length, num_nodes, space_to_trailing_load, distributed_load):
    V_max = []
    V_min = []
    M = []
    dx = span_length/num_nodes
    x = 0
    add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
        distributed_load, span_length)
    #makes updating the location of the axle easier
    axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    abs_axle_location = get_abs_axle_location(axle_spacing)
    num_axles = len(axle_wt)
    axle_num = get_axle_num(num_axles)

    while x <= span_length:
        maxV = 0.0
        minV = 0.0
        maxM = 0.0
        prev_axle_loc = []
        for axle_id in axle_num:
            #calc current location of all axles on span with the axle_id axle over the current node
            cur_axle_loc = move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc, num_axles)

            Pt, xt, Pl, xl, Pr, xr = load_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles)


            Ra = Pt*((span_length-xt)/span_length)
            Rb = Pt*(xt/span_length)
            
            Vac = Rb - Pr 
            Vbc = Pl - Ra


            if Vac < 0:
                if Vac < minV:
                    minV = Vac
            if Vac >= 0:
                if Vac > maxV:
                    maxV = Vac 

            if Vbc < 0:
                if Vbc < minV:
                    minV = Vbc
            if Vbc >= 0:
                if Vbc > maxV:
                    maxV = Vbc

            e = x - xl 
            Mc = Ra*x - Pl*e
            if Mc > maxM:
                maxM = Mc
            
            prev_axle_loc = cur_axle_loc
            #print "prev_axle_loc: " + str(prev_axle_loc)
        x = x + dx

        V_max.append(maxV)
        V_min.append(minV)
        M.append(maxM)
    
    print max(V_max)/2
    print min(V_min)/2
    print max(M)/2

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
    
def load_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles):
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
        if cur_axle_loc[i] >= 0 and cur_axle_loc[i] <= span_length:
            Pt = Pt + axle_wt[i]
            sum_Ptx = sum_Ptx + cur_axle_loc[i]*axle_wt[i]

        if cur_axle_loc[i] >= 0.0 and cur_axle_loc[i] <= x:
            Pl = Pl + axle_wt[i]
            sum_Plx = sum_Plx + cur_axle_loc[i]*axle_wt[i]

        if cur_axle_loc[i] >= x and cur_axle_loc[i] <= span_length:
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
        distributed_load, span_length):
    """Approximates the distributed trailing load as closely spaced point
    loads."""

    #approximate a distributed trailing load as closely spaced point loads
    #each point load is the distributed load times the point load spacing
    #the point load spacing is a function of the span lenght and number of
    #divisions required
    

    pt_load_spacing = 0.5
    num_loads = int(span_length/pt_load_spacing)
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
    span_length = 189.0
    num_nodes = 20.0

    run_load_left_to_right(axle_spacing, axle_wt,
        span_length, num_nodes, space_to_trailing_load, distributed_load)
    

'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
