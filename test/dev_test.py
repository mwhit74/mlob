# -*- coding: utf-8 -*-
from ml.user_input import get_input
from ml.output import write_output
from ml.mlob import analyze_vehicle
import timeit
import pdb
import matplotlib.pyplot as plt

"""
To run dev_test.py
1. Navigate to moving_loads directory
2. python -m test.dev_test
"""

def manager():
    """Controls the global program execution.

    Calls the user_input module to get the input from the user.

    Runs the mlob routine to generate the internal forces.

    Calls the output module to write the output to the user.
    """
     
    #testing input
    axle_spacing1 = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00, 5.00]
    axle_wt1 = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00, 52.00, 52.00]
    sf1 = 80.0/80.0 #scale factor
    axle_wt1 = [round(sf1*p,3) for p in axle_wt1]
    space_to_trailing_load1 = 5.00
    distributed_load1 = 8.00
    distributed_load1 = round(sf1*distributed_load1,3)

    axle_spacing2 = [5.0, 6.0,5.0]
    axle_wt2 = [100.0, 100.0, 100.0, 100.0]
    space_to_trailing_load2 = 0.0
    distributed_load2 = 0.0


    span_length1_1 = 74.00
    span_length2_1 = 34.00

    span_length1_2 = 74.00
    span_length2_2 = 34.00

    #num_nodes should always be odd to place a node at midspan and at 
    #each support
    #a minimum of 21 nodes should be used for analysis
    num_nodes = 21

    asps = [axle_spacing1, axle_spacing2]
    awts = [axle_wt1, axle_wt2]
    sttls = [space_to_trailing_load1, space_to_trailing_load2]
    dls = [distributed_load1, distributed_load2]

    sls = [[span_length1_1, span_length2_1]]
     
    #asps = [axle_spacing1]
    #awts = [axle_wt1]
    #sttls = [space_to_trailing_load1]
    #dls = [distributed_load1]

    #sls = [[span_length1_1, span_length2_1]]
    #(axle_spacing, axle_wt, space_to_trailing_load, distributed_load, 
    #span_length1, span_length2, num_nodes) = get_input()

    for asp, awt, sttl, dl in zip(asps, awts, sttls, dls):
        for sl in sls:
            axle_spacing = asp
            axle_wt = awt
            space_to_trailing_load = sttl
            distributed_load = dl
            span_length1 = sl[0]
            span_length2 = sl[1]

            #for echoing user input in the output
            uias = [] #user_input_axle_spacing
            [uias.append(x) for x in axle_spacing]
            uiaw = [] #user_input_axle_wt
            [uiaw.append(x) for x in axle_wt]

            start = timeit.default_timer()
            #pdb.set_trace()
            (node_loc, 
             V_max1, M_corr1, V_max1_axle,
             M_max1, V_corr1, M_max1_axle,
             V_max2, M_corr2, V_max2_axle,
             M_max2, V_corr2, M_max2_axle,
             Rmax_pier, Rmax_pier_axle,
            span1_begin, span2_begin) = analyze_vehicle(axle_spacing, axle_wt,
                                                       span_length1, span_length2,
                                                       num_nodes,
                                                       space_to_trailing_load, 
                                                       distributed_load)
            stop = timeit.default_timer()

            analysis_time = stop - start

            write_output(uias, uiaw, span_length1, span_length2, num_nodes,
                    space_to_trailing_load, distributed_load, node_loc, 
                    V_max1, M_corr1, V_max1_axle,
                    M_max1, V_corr1, M_max1_axle,
                    V_max2, M_corr2, V_max2_axle,
                    M_max2, V_corr2, M_max2_axle,
                    Rmax_pier, Rmax_pier_axle,
                    analysis_time, span1_begin, span2_begin)

            #graph(node_loc, V_max1, M_max1, V_max2, M_max2)

def graph(node_loc, V_max1, M_max1, V_max2, M_max2):
    node_loc = node_loc[:(len(node_loc)/2+1)]
    plt.figure(1)
    plt.subplot(211)
    plt.plot(node_loc, V_max1)
    plt.subplot(212)
    plt.plot(node_loc, V_max2)
    plt.show()


if __name__ == "__main__":
    manager()
