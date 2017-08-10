import mlob

def user_verification():
    """Runs two tests one for E80 and one for Alternate."""
    test_e80()
    test_alt()



def test_e80():
    """Setup input for E80 Live Load

    Inputs the E80 loading including a trailing loading with the following inputs:
    
    span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
               18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
               60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
               200.0,250.0,300.0,350.0,400.0]
    
    axle_spacing_e80 = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00,
                        5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00,
                        5.00, 6.00, 5.00]
    axle_wt_e80 = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00,
                   52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00,
                   52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load_e80 = 5.0
    distributed_load_e80 = 8.0
    num_user_nodes = 21

    Args:
        None

    Returns:
        None

    Notes:
        Outputs results
    """
    span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
               18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
               60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
               200.0,250.0,300.0,350.0,400.0]
    
    axle_spacing_e80 = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00,
                        5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00,
                        5.00, 6.00, 5.00]
    axle_wt_e80 = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00,
                   52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00,
                   52.00, 52.00, 52.00, 52.00]
    space_to_trailing_load_e80 = 5.0
    distributed_load_e80 = 8.0
    num_user_nodes = 21

    max_moment_e80 = [50.00,60.00,70.00,80.00,93.89,112.50,
                      131.36,160.00,190.00,220.00,280.00,
                      340.00,412.50,570.42,730.98,910.85,
                      1097.30,1311.30,1601.20,1901.80,2233.10,
                      2597.80,3415.00,4318.90,5339.10,6446.30,
                      9225.40,12406.00,15908.00,19672.00,23712.00,
                      35118.00,48800.00,65050.00,83800.00]
    max_moment_qtr_pt_e80 = [37.50,45.00,55.00,70.00,85.00,100.00,
                             115.00,130.00,145.00,165.00,210.00,
                             255.00,300.00,420.00,555.00,692.50,
                             851.50,1010.50,1233.60,1473.00,1732.30,
                             2010.00,2608.20,3298.00,4158.00,5060.50,
                             7098.00,9400.00,11932.00,14820.00,
                             17990.00,27154.00,38246.00,51114.00,
                             65588.00]
    max_shear_end_e80 = [40.00,46.67,51.43,55.00,57.58,60.00,65.45,
                         70.00,73.84,77.14,85.00,93.33,100.00,110.83,
                         120.86,131.44,141.12,150.80,163.38,174.40,
                         185.31,196.00,221.04,248.40,274.46,300.00,
                         347.35,392.59,436.51,479.57,522.01,626.41,
                         729.34,831.43,933.00]
    max_shear_qtr_pt_e80 = [None,30.00,31.43,35.00,37.78,40.00,
                            41.82,43.33,44.61,47.14,52.50,56.67,
                            60.00,70.00,77.14,83.12,88.90,93.55,
                            100.27,106.97,113.58,120.21,131.89,
                            143.41,157.47,173.12,202.19,230.23,
                            265.51,281.96,306.81,367.30,426.37,
                            484.67,542.40]
    max_shear_ctr_e80 = [20.00,20.00,20.00,20.00,20.00,20.00,
                         21.82,23.33,24.61,25.71,27.50,28.89,
                         28.70,31.75,34.29,37.50,41.10,44.00,
                         45.90,49.73,52.74,55.69,61.45,67.41,
                         73.48,78.72,88.92,101.64,115.20,128.12,
                         140.80,170.05,197.93,225.51,252.44]
    max_pier_reac_e80 = [40.00,53.33,62.86,70.00,75.76,80.00,
                         87.28,93.33,98.46,104.29,113.74,121.33,
                         131.10,147.92,164.58,181.94,199.06,
                         215.90,237.25,257.52,280.67,306.42,
                         354.08,397.70,437.15,474.24,544.14,
                         614.91,687.50,762.22,838.00,1030.40,
                         1225.30,1421.70,1619.00]


    run_vehicle(span_lengths,
                axle_spacing_e80,
                axle_wt_e80,
                num_user_nodes,
                space_to_trailing_load_e80,
                distributed_load_e80,
                max_moment_e80,
                max_moment_qtr_pt_e80,
                max_shear_end_e80,
                max_shear_qtr_pt_e80,
                max_shear_ctr_e80,
                max_pier_reac_e80)


def test_alt():
    """Setup input for running Alternate Live Load.

    Inputs the Alternate loading with the following inputs:

    span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
               18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
               60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
               200.0,250.0,300.0,350.0,400.0]

    axle_spacing_alt = [5.00, 6.00, 5.00]
    axle_wt_alt = [100.00, 100.00, 100.00, 100.00]
    space_to_trailing_load_alt = 0.0
    distributed_load_alt = 8.0
    num_user_nodes = 21

    Args:
        None

    Returns:
        None

    Notes:
        Outputs results
    """
    span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
               18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
               60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
               200.0,250.0,300.0,350.0,400.0]

    axle_spacing_alt = [5.00, 6.00, 5.00]
    axle_wt_alt = [100.00, 100.00, 100.00, 100.00]
    space_to_trailing_load_alt = 0.0
    distributed_load_alt = 8.0
    num_user_nodes = 21
    
    max_moment_alt = [62.50,75.00,87.50,100.00,117.36,140.63,
                      164.20,188.02,212.83,250.30,325.27,400.24,
                      475.00,668.75,866.07,1064.06,1262.50,1461.25,
                      1710.00,1959.00]
    max_moment_qtr_pt_alt = [46.88,56.25,68.75,87.50,106.25,125.00,
                             143.75,162.50,181.25,200.00,250.00,
                             318.79,362.50,500.00,650.00,800.00,
                             950.00,1100.00,1287.48,1481.05]
    max_shear_end_alt = [50.00,58.33,64.29,68.75,72.22,75.00,77.27,
                         83.33,88.46,92.86,100.00,111.11,120.00,
                         133.33,142.86,150.00,155.56,160.00,164.44]
    max_shear_qtr_pt_alt = [None,37.50,39.29,43.75,47.23,50.00,
                            52.28,54.17,55.76,57.14,62.50,68.05,
                            72.50,83.33,92.86,100.00,105.56,
                            110.00,114.45,118.42,120.91,123.33]
    max_shear_ctr_alt = [25.00,25.00,25.00,25.00,25.00,25.00,
                         27.28,29.17,30.76,32.14,34.38,36.11,
                         37.50,41.67,46.43,50.00,55.56,60.00,
                         64.45,68.00,70.91,73.33,77.14,80.00,
                         82.22,84.00]
    max_pier_reac_alt = [50.00,58.33,71.43,81.25,88.89,95.00,
                         100.00,108.33,115.39,121.43,131.25,
                         138.89,145.00,154.17]

    run_vehicle(span_lengths,
                axle_spacing_alt,
                axle_wt_alt,
                num_user_nodes,
                space_to_trailing_load_alt,
                distributed_load_alt,
                max_moment_alt,
                max_moment_qtr_pt_alt,
                max_shear_end_alt,
                max_shear_qtr_pt_alt,
                max_shear_ctr_alt,
                max_pier_reac_alt)


def run_vehicle(span_lengths, axle_spacing, axle_wt, num_user_nodes, space_to_trailing_load,
        distributed_load, cl_max_moment, cl_max_moment_qtr_pt, cl_max_shear_end,
        cl_max_shear_qtr_pt, cl_max_shear_ctr, cl_max_pier_reac):
    """Runs program input for a series of span lenghts and outputs the results.

    Args:
        span_lengths (list of floats): all the span lengths to be run
        axle_spacing (list of floats): the spacing between each axle
        axle_wt (list of floats): weight of each axle
        num_user_nodes (int): number of analysis nodes input by the user
        space_to_trailing_load (float): distance from last discrete axle to
                                        beginning of distributed load
        distributed_load (float): uniformly distributed trailing load magnitude
        cl_max_moment (list of floats): max moment in span from AREMA Table
        cl_max_moment_qtr_pt (list of floats): max moment at 1/4 point of span
                                               from AREMA Table
        cl_max_shear_end (list of floats): max shear at end of span from AREMA
                                           Table
        cl_max_shear_qtr_pt (list of floats): max shear at 1/4 point of span
                                              from AREMA Table 
        cl_max_shear_ctr (list of floats): max shear at center of span from
                                           AREMA Table
        cl_max_pier_reac (list of floats): max pier (or floorbeam) reaction
                                           for equal length, adjacent spans from
                                           AREMA Table

    Returns:
        None

    Notes:
        1. Outputs values from program for each span length
        2. Outputs values from AREMA Table for each span length
        3. Outputs the error of the program with respect to the AREMA Table
           values where possible. (The AREMA Tables are incomplete.)
    """
    header = "{0:^15} {1:^15} {2:^15} {3:^15} {4:^15} {5:^15} {6:^15} {7:^15}".format("Type",
                                            "Span Length [ft]",
                                            "Max M [ft-kip]",
                                            "Max M 1/4 Pt [ft-kip]",
                                            "Max V End [kip]",
                                            "Max V 1/4 Pt [kip]",
                                            "Max V Ctr [kip]",
                                            "Max Rpier [kip]")
    print header
                                     
    for i in range(len(span_lengths)):
        span_length = span_lengths[i]
        (node_loc, V_max1, M_max1, V_max2, M_max2, Rmax_pier,
        span1_begin, span2_begin) = mlob.analyze_vehicle(axle_spacing,
                                                        axle_wt,
                                                        span_length,
                                                        span_length,
                                                        num_user_nodes,
                                                        space_to_trailing_load,
                                                        distributed_load)
        max_moment = max(M_max1)/2
        max_moment_q = M_max1[5]/2
        max_shear_e = V_max1[0]/2
        max_shear_q = V_max1[5]/2
        max_shear_c = V_max1[10]/2
        r_max_pier = Rmax_pier/2

        out = ("{0:^15s} {1:^15.3f} {2:^15.3f} {3:^22.3f} {4:^15.3f}" +
               "{5:^17.3f} {6:^15.3f} {7:^15.3f}").format("Progam Output",
                                             span_length,
                                             max_moment,
                                             max_moment_q,
                                             max_shear_e,
                                             max_shear_q,
                                             max_shear_c,
                                             r_max_pier)

        print out

        try:
            c_max_moment = "{0:.3f}".format(cl_max_moment[i])
            e_max_moment = "{0:.3f}".format(error(cl_max_moment[i], max_moment))
        except IndexError as e:
            c_max_moment = ""
            e_max_moment = ""

        try:
            c_max_moment_q = "{0:.3f}".format(cl_max_moment_qtr_pt[i])
            e_max_moment_q = "{0:.3f}".format(error(cl_max_moment_qtr_pt[i],
                                                    max_moment_q))
        except IndexError as e:
            c_max_moment_q = ""
            e_max_moment = ""

        try:
            c_max_shear_e = "{0:.3f}".format(cl_max_shear_end[i])
            e_max_shear_e = "{0:.3f}".format(error(cl_max_shear_end[i], max_shear_e))
        except IndexError as e:
            c_max_shear_e = ""
            e_max_shear_e = ""

        try:
            c_max_shear_q = cl_max_shear_qtr_pt[i]
            if c_max_shear_q == None:
                c_max_shear_q = ""
                e_max_shear_q = ""
            else:
                c_max_shear_q = "{0:.3f}".format(cl_max_shear_qtr_pt[i])
                e_max_shear_q = "{0:.3f}".format(error(cl_max_shear_qtr_pt[i],
                                                 max_shear_q))
        except IndexError as e:
            c_max_shear_q = ""
            e_max_shear_q = ""

        try:
            c_max_shear_c = "{0:.3f}".format(cl_max_shear_ctr[i])
            e_max_shear_c = "{0:.3f}".format(error(cl_max_shear_ctr[i], max_shear_c))
        except IndexError as e:
            c_max_shear_c = ""
            e_max_shear_c = ""

        try:
            c_r_max_pier = "{0:.3f}".format(cl_max_pier_reac[i])
            e_r_max_pier = "{0:.3f}".format(error(cl_max_pier_reac[i], r_max_pier))
        except IndexError as e:
            c_r_max_pier = ""
            e_r_max_pier = ""


        out = ("{0:^15s} {1:^15.3f} {2:^15s} {3:^22s} {4:^15s}" +
               "{5:^17s} {6:^15s} {7:^15s}").format("AREMA Tb",
                                             span_length,
                                             c_max_moment,
                                             c_max_moment_q,
                                             c_max_shear_e,
                                             c_max_shear_q,
                                             c_max_shear_c,
                                             c_r_max_pier)

        print out

        out = ("{0:^15s} {1:^15.3f} {2:^15s} {3:^22s} {4:^15s}" +
               "{5:^17s} {6:^15s} {7:^15s}").format("Error",
                                             span_length,
                                             e_max_moment,
                                             e_max_moment_q,
                                             e_max_shear_e,
                                             e_max_shear_q,
                                             e_max_shear_c,
                                             e_r_max_pier)

        print out

        print "\n"

def error(v1, v2):
    """Returns the relative error with respect to the first value."""

    e = abs(v1 - v2)/v1
    return e

if __name__ == "__main__":
    user_verification()
