def write_output(axle_spacing, axle_wt, span_length1, span_length2, num_nodes,
           space_to_trailing_load, distributed_load, node_loc, V_max1,
           M_max1, V_max2, M_max2, Rmax_pier, analysis_time,
           span1_begin, span2_begin):
    """Format and print output."""
    #currently outputs half track (one rail)
    echo_input = ""
    out_tb = ""
    out_val = ""
  
    echo_input += "\n\nECHO INPUT\n"
    echo_input += "Axle spacing: " + str(axle_spacing) + "\n"
    echo_input += "Axle weights: " + str(axle_wt) + "\n"
    echo_input += "Length Span 1: " + str(span_length1) + "\n"
    echo_input += "Length Span 2: " + str(span_length2) + "\n"
    echo_input += "Number of Nodes: " + str(num_nodes) + "\n"
    echo_input += "Space to trailing load: " + str(space_to_trailing_load) + "\n"
    echo_input += "Distributed trailing load: " + str(distributed_load) + "\n"
  
  
    out_tb += "\n\nOUTPUT\n"
    out_tb += "SPAN 1"
    out_tb += "\n" #span 1 title spacing
    out_tb += "{0:^15s}{1:^15s}{2:^15s}".format("x",
                                                "Vmax",
                                                "Mmax")
    out_tb += "\n" #span 1 header spacing
  
    for x,Vmax,Mmax in zip(node_loc, V_max1, M_max1):
        out_tb += """{0:^-15.3f}{1:^-15.3f}{2:^-15.3f}\n""".format(x,
                                                                   Vmax/2,
                                                                   Mmax/2)
  
    out_tb += "\n" #span 1 table spacing
  
  
    out_val += """Span 1 Vmax: {0:<-.3f}\n Span 1 Mmax: {1:<-.3f}""".format(max(V_max1)/2,
                                                                            max(M_max1)/2)
    out_val += "\n" #span 1 max/min spacing
  
  
    if V_max2 != []:
        out_tb += "SPAN 2"
        out_tb += "\n" #span 2 title spacing
        out_tb += "{0:^15s}{1:^15s}{2:^15s}".format("x",
                                                    "Vmax",
                                                    "Mmax")
        out_tb += "\n" #span 2 header spacing
  
        for x,Vmax,Mmax in zip(node_loc, V_max2, M_max2):
            out_tb += """{0:^-15.3f}{1:^-15.3f}{2:^-15.3f}\n""".format(x,
                                                                       Vmax/2,
                                                                       Mmax/2)
  
        out_tb += "\n\n" #span 2 table spacing
        
        out_val += """Span 2 Vmax: {0:<-.3f}\nSpan 2 Mmax: {1:<-.3f}""".format(max(V_max2)/2,
                                                                                max(M_max2)/2)
  
        out_val += "\nRmax pier or floorbeam: {0:<-.3f}".format(Rmax_pier/2)
      
    print echo_input + out_tb + out_val
       
    print "Runtime [sec]: {0:<.3f}\n\n".format(analysis_time)


