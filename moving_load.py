

def main(num_axles, axle_num, axle_spacing, axle_wt, span_length, num_nodes):
    V_max = []
    V_min = []
    M = []
    dx = span_length/num_nodes
    x = 0 
    #makes updating the location of the axle easier
    axle_spacing.insert(0, 0.0)
    abs_axle_spacing = get_abs_axle_spacing(axle_spacing)

    while x <= span_length:
        maxV = 0.0
        minV = 0.0
        maxM = 0.0
        prev_axle_loc = []
        print "x: " + str(x)
        for axle_id in axle_num:
            print "axle_id: " + str(axle_id)
            #calc current location of all axles on span with the axle_id axle over the current node
            cur_axle_loc = move_axle_loc(x, axle_spacing, abs_axle_spacing, axle_id, prev_axle_loc, num_axles)
            #print "cur_axle_loc: " + str(cur_axle_loc)
            Pt, xt = total_load_and_loc(cur_axle_loc, axle_wt, span_length, num_axles)
            Pl, xl = load_to_left_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles)
            Pr, xr = load_to_right_and_loc(cur_axle_loc, axle_wt, x, span_length, num_axles)


            Ra = Pt*((span_length-xt)/span_length)
            Rb = Pt*(xt/span_length)
            
            #Va =  
            Vc = Ra - Pl
            print "Vc: " + str(Vc)
            if Vc < 0:
                if Vc < minV:
                    minV = Vc
            if Vc >= 0:
                if Vc > maxV:
                    maxV = Vc     
            '''
            #not sure what 'a' is yet
            Mc = Pt*(xt/span_length)*a - Pl*xl
            if Mc > maxM:
                maxM = Mc
            '''
            prev_axle_loc = cur_axle_loc
            #print "prev_axle_loc: " + str(prev_axle_loc)
        x = x + dx

        V_max.append(maxV)
        V_min.append(minV)
        #M.append(maxM)
    
    print V_max
    print V_min

def get_abs_axle_spacing(axle_spacing):
    abs_axle_spacing = []

    loc = 0.00 #initialize

    for spacing in axle_spacing:
        loc = loc + spacing 
        abs_axle_spacing.append(loc)

    return abs_axle_spacing          

#updating the location of each axle             
def move_axle_loc(x, axle_spacing, abs_axle_spacing, axle_id, prev_axle_loc, num_axles):
    cur_axle_loc = []
    
    for i in range(num_axles):
        if axle_id == 1 and i == 0:
            #sets the initial locaction of the first axle
            axle_loc = x
        elif axle_id == 1 and i > 0:
            #sets the intial location of all subsequent axles
            axle_loc = x - abs_axle_spacing[i]
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

    if Pt == 0:
        xt = 0
    else:        
        xt = sum_Px/Pt

    print "Pt: " + str(Pt)
    print "xt: " + str(xt)

    return Pt, xt
    
def load_to_left_and_loc(cur_axle_loc, axle_wts, x, span_length, num_axles):
    Pl = 0.0
    xl = 0.0
    sum_Px = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= 0.0 and cur_axle_loc[i] <= x:
            Pl = Pl + axle_wts[i]
            sum_Px = sum_Px + cur_axle_loc[i]*axle_wts[i]
    
    if Pl == 0:
        xl = 0
    else:        
        xl = sum_Px/Pl

    print "Pl: " + str(Pl)
    print "xl: " + str(xl)
    
    return Pl, xl

def load_to_right_and_loc(cur_axle_loc, axle_wts, x, span_length, num_axles):
    Pr = 0.0
    xr = 0.0
    sum_Px = 0.0
    
    for i in range(num_axles):
        if cur_axle_loc[i] >= x and cur_axle_loc[i] <= span_length:
            Pr = Pr + axle_wts[i]
            sum_Px = sum_Px + cur_axle_loc[i]*axle_wts[i]
    
    if Pr == 0:
        xr = 0
    else:        
        xr = sum_Px/Pr

    print "Pr: " + str(Pr)
    print "xr: " + str(xr)
    
    return Pr, xr

def get_axle_num(num_axles):
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num
        
        
                
if __name__ == "__main__":
    #input
    #axle_spacing = [8.00, 13.00, 18.00, 23.00, 32.00, 37.00, 43.00, 48.00, 56.00, 64.00, 69.00, 74.00, 79.00, 88.00, 93.00, 99.00, 104.00]
    #axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    axle_spacing = []
    axle_wt = [1.0]
    num_axles = len(axle_wt)
    axle_num = get_axle_num(num_axles)
    span_length = 20.0
    num_nodes = 20.0 
    
    main(num_axles, axle_num, axle_spacing, axle_wt, span_length, num_nodes)
    










'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
