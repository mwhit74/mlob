

def main(num_axles, axle_num, axle_spacing, axle_wt, span_length, num_nodes):
    V_max = []
    V_min = []
    M = []
    dx = span_length/num_nodes
    x = 0 
    #makes updating the location of the axle easier
    axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    abs_axle_location = get_abs_axle_location(axle_spacing)

    while x <= span_length:
        maxV = 0.0
        minV = 0.0
        maxM = 0.0
        prev_axle_loc = []
        for axle_id in axle_num:
            #calc current location of all axles on span with the axle_id axle over the current node
            cur_axle_loc = move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc, num_axles)

            Pt, xt = total_load_and_loc(cur_axle_loc, axle_wt, span_length, num_axles)
            Pl, xl = load_to_left_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles)
            Pr, xr = load_to_right_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles)


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
    
    print max(V_max)
    print min(V_min)
    print max(M)

def get_abs_axle_location(axle_spacing):
    abs_axle_location = []

    loc = 0.00 #initialize

    for spacing in axle_spacing:
        loc = loc + spacing 
        abs_axle_location.append(loc)

    return abs_axle_location          

#updating the location of each axle             
def move_axle_loc(x, axle_spacing, abs_axle_location, axle_id, prev_axle_loc, num_axles):
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
    
def total_load_and_loc(cur_axle_loc, axle_wt, span_length, num_axles):
    Pt = 0.0
    xt = 0.0
    sum_Px = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= 0 and cur_axle_loc[i] <= span_length:
            Pt = Pt + axle_wt[i]
            sum_Px = sum_Px + cur_axle_loc[i]*axle_wt[i]
    
    #avoid divide by zero error
    if Pt == 0:
        xt = 0
    else:        
        xt = sum_Px/Pt

    return Pt, xt
    
def load_to_left_and_loc(cur_axle_loc, axle_wts, x, span_length, num_axles):
    Pl = 0.0
    xl = 0.0
    sum_Px = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= 0.0 and cur_axle_loc[i] <= x:
            Pl = Pl + axle_wts[i]
            sum_Px = sum_Px + cur_axle_loc[i]*axle_wts[i]

    #avoid divide by zero error
    if Pl == 0:
        xl = 0
    else:        
        xl = sum_Px/Pl

    return Pl, xl

def load_to_right_and_loc(cur_axle_loc, axle_wts, x, span_length, num_axles):
    Pr = 0.0
    xr = 0.0
    sum_Px = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= x and cur_axle_loc[i] <= span_length:
            Pr = Pr + axle_wts[i]
            sum_Px = sum_Px + cur_axle_loc[i]*axle_wts[i]
    
    #avoid divide by zero error
    if Pr == 0:
        xr = 0
    else:        
        xr = sum_Px/Pr

    return Pr, xr

def get_axle_num(num_axles):
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num
        
        
                
if __name__ == "__main__":
    #input
    axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    #axle_spacing = []
    #axle_wt = [1.0]
    num_axles = len(axle_wt)
    axle_num = get_axle_num(num_axles)
    span_length = 20.0
    num_nodes = 100.0 
    
    main(num_axles, axle_num, axle_spacing, axle_wt, span_length, num_nodes)
    










'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
