

def main(num_axles, axle_num, axle_config, axle_wt, span_length, num_nodes):
    V = []
    M = []
    dx = span_length/num_nodes
    x = 0 
    while x <= span_length:
        maxV = 0.0
        maxM = 0.0
        print x
        prev_axle_config = axle_config
        for axle_id in axle_num:
            print axle_id
            cur_axle_config = move_axle_config(x, prev_axle_config, num_axles)
            print cur_axle_config
            #Pt, xt = total_load_and_loc(cur_axle_config, axle_wts)
            #Pl, xl = load_to_right_and_loc(cur_axle_config, axle_wts, x)
            ''' 
            Vc = Pt*(xt/span_length) - Pl
            if Vc > maxV:
                maxV = Vc
                
            
            #not sure what 'a' is yet
            Mc = Pt*(xt/span_length)*a - Pl*xl
            if Mc > maxM:
                maxM = Mc
            '''
            prev_axle_config = cur_axle_config
        x = x + dx

        #V.append(maxV)
        #M.append(maxM)

            
            
            
def move_axle_config(x, prev_axle_config, num_axles):
    cur_axle_config = []
    
    for i in range(num_axles):
        axle_loc = x + prev_axle_config[i]
        cur_axle_config.append(axle_loc)
        
    return cur_axle_config
    
def total_load_and_loc(cur_axle_config, axle_wts):
    Pt = 0.0
    xt = 0.0
    
    for i in range(len(cur_axle_config)):
        if cur_axle_config[i] >= 0:
            Pt = Pt + axle_wts[i]
            sum_Px = cur_axle_config[i]*axle_wts[i]
            
    xt = sum_Px/Pt
    
    return Pt, xt
    
def load_to_right_and_loc(cur_axle_config, axle_wts, x):
    Pl = 0.0
    xl = 0.0
    
    for i in range(len(cur_axle_config)):
        if cur_axle_config[i] >= x:
            Pl = Pl + axle_wts[i]
            sum_Px = cur_axle_config[i]*axle_wts[i]
            
    xl = sum_Px/Pl
    
    return Pl, xl

def get_axle_num(num_axles):
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num
        
        
                
if __name__ == "__main__":
    #input
    #axle spacing must always start at 0.0, the spacing from axle 0 to axle 0 is 0.0
    axle_config = [0.00, 8.00, 13.00, 18.00, 23.00, 32.00, 37.00, 43.00, 48.00, 56.00, 64.00, 69.00, 74.00, 79.00, 88.00, 93.00, 99.00, 104.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    num_axles = len(axle_config)
    axle_num = get_axle_num(num_axles)
    span_length = 60.0
    num_nodes = 20.0
    
    main(num_axles, axle_num, axle_config, axle_wt, span_length, num_nodes)
    










'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
