# -*- coding: utf-8 -*-
from user_input import get_input
from output import write_output
from mlob import analyze_vehicle
import timeit
import pdb

def manager():

     
    #input
    axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load = 5.00
    distributed_load = 8.00
    #axle_spacing = []
    #axle_wt = [1.0]
    span_length1 = 7.0
    span_length2 = 7.0
    #num_nodes should always be odd to place a node at midspan and at 
    #each support
    #a minimum of 21 nodes should be used for analysis
    num_nodes = 51
     

    #axle_spacing, axle_wt, space_to_trailing_load, distributed_load, \
    #span_length1, span_length2, num_nodes = get_input()

    uias = [] #user_input_axle_spacing
    [uias.append(x) for x in axle_spacing]
    uiaw = [] #user_input_axle_wt
    [uiaw.append(x) for x in axle_wt]

    start = timeit.default_timer()
    node_loc, V_max1, M_max1, V_max2, M_max2, Rmax_pier,\
    span1_begin, span2_begin = analyze_vehicle(axle_spacing, axle_wt,
                                               span_length1, span_length2,
                                               num_nodes,
                                               space_to_trailing_load, 
                                               distributed_load)

    stop = timeit.default_timer()

    analysis_time = stop - start
    write_output(uias, uiaw, span_length1, span_length2, num_nodes,
            space_to_trailing_load, distributed_load, node_loc, V_max1,
            M_max1, V_max2, M_max2, Rmax_pier, analysis_time,
            span1_begin, span2_begin)

if __name__ == "__main__":
    manager()
