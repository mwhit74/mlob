

def main(axle_num, axle_config, axle_wt, span_length, num_nodes, nodes, steps):
    V = []
    M = []
    for x in nodes:
        maxV = 0.0
        maxM = 0.0
        for axle_id in axle_num:
            cur_axle_config = move_axle_config(x, axle_id, axle_config)
            Pt, xt = total_load_and_loc(cur_axle_config, axle_wts)
            Pl, xl = load_to_right_and_loc(cur_axle_config, axle_wts, x)
            
            Vc = Pt*(xt/span_length) - Pl
            if Vc > maxV:
                maxV = Vc
                
            '''
            #not sure what 'a' is yet
            Mc = Pt*(xt/span_length)*a - Pl*xl
            if Mc > maxM:
                maxM = Mc
            '''

        V.append(maxV)
        M.append(maxM)

            
            
            
def move_axle_config(y1, axle_config):
    cur_axle_config = []
    
    for i in range(len(axle_config)):
        axle_loc = y1 - axle_config[i]
        cur_axle_config.append(axle_loc)
        
    return cur_axle_config
    
def total_load_and_loc(cur_axle_config, axle_wts):
    Pt = 0.0
    xt = 0.0
    
    for i in range(len(cur_axle_config):
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
        
        
                
if __name__ = "__main__":
    #input
    axle_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    axle_config = [0.00, 8.00, 13.00, 18.00, 23.00, 32.00, 37.00, 43.00, 48.00, 56.00, 64.00, 69.00, 74.00, 79.00, 88.00, 93.00, 99.00, 104.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    span_length = 60.0
    num_nodes = 20.0
    nodes = [0.0]
    nodes.append([span_length/num_nodes + nodes[x-1] for x in range(num_nodes)])
    step = 2.0
    steps = [0.0]
    steps.append([step + steps[x-1] for x in range((span_length+axle_config[-1])/step)])
    
    main(axle_num, axle_config, axle_wt, span_length, num_nodes, nodes, steps)
    










'''
class Axle():
    def __init__(self, axle_loc, axle_wt):
        self.axle_loc = axle_loc
        self.axle_wt = axle_wt
'''
        

            
            
        
