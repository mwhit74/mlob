# -*- coding: utf-8 -*-
from user_input import get_input, user_option
from output import write_output
from mlob import analyze_vehicle
from user_test import user_verification
import timeit
import pdb

def manager():
    """Controls the program execution.

    Allows the user to select between analysis and verification. 

    If analysis is chosen the user_input module is called to get the input
    from the user. The mlob routine is run to generate the internal forces.
    Finally the output module is passed the user input and program output
    to write the output to the user.

    If the verification is chosen the verification routine is run which compares
    AREMA Tb 15-1-16 values to the program calculated values. Both values are
    reported for each span length specified in the AREMA table and the relative
    error between the table value and program value.

    Args:
        None

    Returns:
        None
    """
    while True:
        option = user_option()

        if option == "a" or option == "A" or option == "Analysis":
            (axle_spacing, axle_wt, space_to_trailing_load, distributed_load, 
            span_length1, span_length2, num_nodes) = get_input()
        
            #for echoing user input in the output
            uias = [] #user_input_axle_spacing
            [uias.append(x) for x in axle_spacing]
            uiaw = [] #user_input_axle_wt
            [uiaw.append(x) for x in axle_wt]

            start = timeit.default_timer()

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
        elif option == "v" or option == "V" or option == "Verify":
            user_verification()
        else:
            print "Invalid command."


if __name__ == "__main__":
    manager()
