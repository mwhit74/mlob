# -*- coding: utf-8 -*-
"""The mlob module calculates the maximum effects of a vehicle on a simply
supported span including the pier reaction for two adjacent simply supported
spans of differing lengths.
"""

def analyze_vehicle(axle_spacing, axle_wt, span_length1, span_length2,
                     num_user_nodes, space_to_trailing_load, distributed_load,
                      point_load_spacing=0.5):
    """Calculates the max shear and moment at each analysis node in 1 or 2 spans.

    This function calculates the maximum shear and moment at each analysis node
    in one or two spans of equal or unequal lengths. This is accomplished by
    iterating through each analysis node, at each analysis node each axle of
    vehicle is placed on the analysis node and the location of all the other
    axles is determined, the moment and shear are calculated for this instance of
    axle locations. This operation is repeated for each axle of the vehicle and
    for each analysis node. The axles are incremented left to right and right to
    left to cover all possible axle locations in either direction.

    Args:
        axle_spacing (list of floats): the spacing between each axle
        axle_wt (list of floats): weight of each axle
        span_length1 (float): length of span 1
        span_length2 (float): length of span 2
        num_user_nodes (int): number of analysis nodes input by the user
        space_to_trailing_load (float): distance from last discrete axle to
                                        beginning of distributed load
        distributed_load (float): uniformly distributed trailing load magnitude
        point_load_spacing (float, optional): spacing of approximate discretely
                                              spaced point loads, 
                                              defaults to 0.5

    Returns:
        node_loc_ltr (list of floats): coordinate location of analysis nodes in
                                       order ltr
        V_max1 (list of floats): maximum shear at each analysis node in span 1
        M_corr1 (list of floats): corresponding moment to maximum shear at each
                                  analysis node in span 1
        M_max1 (list of floats): maximum moment at each analysis node in span 1
        V_corr1 (list of floats): corresponding shear to maximum moment at each
                                  analysis node in span 1
        V_max2 (list of floats): maximum moment at each analysis node in span 2
        M_corr22 (list of floats): corresponding moment to maximum shear at each
                                  analysis node in span 2
        M_max2 (list of floats): maximum moment at each analysis node in span 2
        V_corr2 (list of floats): corresponding shear to maximum moment at each
                                  analysis node in span 2
        Rmax_pier (list of floats): maximum pier reaction, 
                                    [max pier reaction, right component,
                                    left component]; returns None if span length
                                    2 is not entered by user
        span1_begin (float): coordinate location of beginning of span 1
        span2_begin (float): coordinate location of beginning of span 2
        
    Notes:
        Placing each axle directly at the analysis node ensures that the maximum
        shear and moment is calculated for each axle and corresponding axle
        locations. While the maximum shear and moment will be calculated for that
        specific analysis node location, the overall maximum shear and moment of the
        span may not be calculated if there is not enough discretization of analysis
        nodes, i.e. not enough analysis nodes in the span to accurately describe the
        shear and moment behavior.
    """
    #calculates for a full track (2 rails)
    V_max1 = []
    M_corr1 = []
    V_max1_axle = []
    M_max1 = []
    V_corr1 = []
    M_max1_axle = []
    V_max2 = []
    M_corr2 = []
    V_max2_axle = []
    M_max2 = []
    V_corr2 = []
    M_max2_axle = []
    Rmax_pier = [None, None, None, None, None]

    (span1_begin,
    span1_end,
    span2_begin,
    span2_end) = span_begin_end_coords(span_length1, span_length2)

    node_loc_ltr = node_location(span1_begin, span1_end, span2_begin,
                                 span2_end, num_user_nodes)
    node_loc_rtl = list(reversed(node_loc_ltr))

    mod_axle_spacing, mod_axle_wt = add_trailing_load(axle_spacing, 
                                              axle_wt, 
                                              space_to_trailing_load,
                                              distributed_load,
                                              span1_begin,
                                              span2_end,
                                              point_load_spacing)
    mod_axle_spacing.insert(0, 0.0) #insert a dummy spacing for the first axle
    num_axles = len(mod_axle_wt) #number of axles in the pattern
    axle_num = number_axles(num_axles) #numbered axles
    for node_loc,direction in zip([node_loc_ltr, 
                                        node_loc_rtl],
                                        ["ltr","rtl"]):
        num_analysis_nodes = len(node_loc)

        #initialize span index id value
        if direction == "ltr":
            span1_index_id = -1
            span2_index_id = -1
        elif direction == "rtl":
            span1_index_id = num_user_nodes
            span2_index_id = num_user_nodes

        #loop thru analysis node locations
        for x,i in zip(node_loc, range(num_analysis_nodes)): 
            Ve1 = 0.0
            M1 = 0.0
            Ve2 = 0.0
            M2 = 0.0

            #calculate span index id value
            if x >= span1_begin and x <= span1_end:
                if direction == "ltr":
                    span1_index_id = span1_index_id + 1
                elif direction == "rtl":
                    span1_index_id = span1_index_id - 1

            if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
                if direction == "ltr":
                    span2_index_id = span2_index_id + 1
                elif direction == "rtl":
                    span2_index_id = span2_index_id - 1

            #loop thru each axle in the axle configuration placing each axle at
            #current analysis node
            for axle_id in axle_num:
                #calculate location of each axle based on the axle currently
                #over the analysis node
                if axle_id == 1:
                    cur_axle_loc = get_abs_axle_location(mod_axle_spacing, x,
                            direction)
                else:
                    prev_axle_loc = cur_axle_loc

                    cur_axle_loc = move_axle_loc(mod_axle_spacing, axle_id,
                                                 prev_axle_loc, num_axles,
                                                 direction)

                Pt1, xt1, Pli1, Ple1, xli1, xle1, Pri1, Pre1, xri1, xre1 = calc_load_and_loc(cur_axle_loc,
                           mod_axle_wt, x, span1_begin, span1_end, num_axles)
                
                Pt2, xt2, Pli2, Ple2, xli2, xle2, Pri2, Pre2, xri2, xre2 = calc_load_and_loc(cur_axle_loc,
                           mod_axle_wt, x, span2_begin, span2_end, num_axles)
               
                Rpier = calc_pier_reaction(cur_axle_loc, mod_axle_wt, span1_begin,
                                    span1_end, span2_begin, span2_end,
                                    num_axles, axle_id, direction)

                Rmax_pier = envelope_pier_reaction(Rmax_pier, Rpier) 
                                                                   
                if x >= span1_begin and x <= span1_end:
                    Rb1, Re1 = calc_reactions(Pt1, xt1, span1_begin, span1_end, direction) 
                    
                    Ve1 = calc_shear(Pt1, xt1, Pli1, Ple1, Pri1, Pre1, direction, span1_begin, span1_end)

                    M1 = calc_moment(x, 
                                     xli1,
                                     xle1,
                                     xri1,
                                     xre1,
                                     span1_begin, 
                                     span1_end, 
                                     Rb1, 
                                     Pli1,
                                     Ple1,
                                     Pri1,
                                     Pre1,
                                     direction,
                                     Pt1,
                                     xt1)
                    
                    envelope_shear(Ve1, V_max1, M1, M_corr1, axle_id,
                                   direction, V_max1_axle, span1_index_id)

                    envelope_moment(M1, M_max1, Ve1, V_corr1, axle_id,
                                    direction, M_max1_axle, span1_index_id)

                if span_length2 != 0.0 and x >= span2_begin and x <= span2_end:
                    Rb2, Re2 = calc_reactions(Pt2, xt2, span2_begin, span2_end, direction)
        
                    Ve2 = calc_shear(Pt2, xt2, Pli2, Ple2, Pri2, Pre2, direction, span2_begin, span2_end)

                    M2 = calc_moment(x, 
                                     xli2,
                                     xle2,
                                     xri2,
                                     xre2,
                                     span2_begin, 
                                     span2_end, 
                                     Rb2, 
                                     Pli2,
                                     Ple2,
                                     Pri2,
                                     Pre2,
                                     direction,
                                     Pt2,
                                     xt2)
        
                    envelope_shear(Ve2, V_max2, M2, M_corr2, axle_id, 
                                   direction, V_max2_axle, span2_index_id)

                    envelope_moment(M2, M_max2, Ve2, V_corr2, axle_id,
                                    direction, M_max2_axle, span2_index_id)


    return (node_loc_ltr,
            V_max1, M_corr1, V_max1_axle,
            M_max1, V_corr1, M_max1_axle,
            V_max2, M_corr2, V_max2_axle,
            M_max2, V_corr2, M_max2_axle,
            Rmax_pier,
            span1_begin, span2_begin)


def calc_reactions(Pt, xt, span_begin, span_end, direction):
    """Calculate span reactions.

    Calculates the reactions at the end of each span. The pier reaction is not
    calculated in this function.
    
    Moving left to right:
        Rb = Pt*(span_end - xt)/span_length
        Re = Pt*(xt - span_begin)/span_length
    Moving right to left:
        Rb = Pt*(xt - span_begin)/span_length
        Re = Pt*(span_end - xt)/span_length

    Args:
        Pt (float): total load on the span
        xt (float): location of the total load on the span
        span_begin (float): span begin coordinate
        span_end (float): span end coordinate
        direction (str): flag to determine which direction is being calculated,
                            either 'ltr' or 'rtl'

    Returns:
        Rb (float): reaction at the beginning of the span
        Re (float): reaction at the end of the span

    Notes:
        For the vehicle moving ltr, Rb is the left span reaction and Re is the
        right span reaction.
        For the vehicle moving rtl, Rb is the right span reaction and Re is the
        left span reaction.
    """
    span_length = span_end - span_begin
    if span_length == 0.0:
        Rb = 0.0
        Re = 0.0
    else:
        if direction == "ltr":
            Rb = Pt*(span_end - xt)/span_length
            Re = Pt*(xt - span_begin)/span_length
        elif direction == "rtl":
            Rb = Pt*(xt - span_begin)/span_length
            Re = Pt*(span_end - xt)/span_length

    return Rb, Re


def calc_pier_reaction(cur_axle_loc, mod_axle_wt, span1_begin, span1_end,
                       span2_begin, span2_end, num_axles, axle_id, direction):
    """Calculate the interior pier (floorbeam) reaction.

    Args:
        cur_axle_loc (list of floats): current x-coordinate of all axles on span
        axle_wt (list of floats): weight of each axle
        begin_span (float): x-coordinate of the beginning of the span
        end_span (float): x-coordinate of the end of the span
        num_axles (int): number of program defined axles (includes axles for
                         approximate distributed load)

    Returns:
        Rpier (float): reaction at the pier (floorbeam)

    Notes:
        This function is very similar to the calc_load_and_loc function. The
        main reason this function is required is the loads that act directly
        over the support at the beginning of span 1 and at the end of span 2 do
        not contribute to the reaction at the pier. However, they do contribute
        to the reactions of each span and in determining the correct moment and
        shear in each span. 
    """
    Rpier = 0.0
    #these are *not* the reactions at the beginning and end supports of a two
    #span structure
    #these are the two reactions on the center pier for the adjacent span
    L_S1 = 0.0 #center pier reaction from loads on span 1
    L_S2 = 0.0 #center pier reaction from loads on span 2

    span1_length = span1_end - span1_begin
    span2_length = span2_end - span2_begin

    for i in range(num_axles):
        #if load is not over the support at the beginning of span 1
        #and if the load is not over the support at the end of span 2
        if cur_axle_loc[i] > span1_begin and cur_axle_loc[i] < span2_end:
            #if axle is directly over pier
            if cur_axle_loc[i] == span1_end:
                r = mod_axle_wt[i]
                L_S1 = L_S1 + r/2
                L_S2 = L_S2 + r/2
            #if the load is on span 1, calc the reaction at the pier
            if cur_axle_loc[i] < span1_end:
                r = (cur_axle_loc[i] - span1_begin)/span1_length*mod_axle_wt[i]
                L_S1 = L_S1 + r
            #if the load is on span 2, calc the reaction at the pier
            if cur_axle_loc[i] > span2_begin:
                r = (span2_end - cur_axle_loc[i])/span2_length*mod_axle_wt[i]
                L_S2 = L_S2 + r

    Rpier = L_S1 + L_S2
            
    return Rpier, L_S1, L_S2, axle_id, direction

def envelope_pier_reaction(Rmax_pier, Rpier):
    """Envelope the maximum interior pier (floorbeam) reaction.
    
    On each iteration compare the maximum pier reaction to the calculated pier
    reaction. If the calculate pier reaction is greater than the maximum,
    replace the maximum.
    """
    if Rpier[0] > Rmax_pier[0]:
        return Rpier
    else:
        return Rmax_pier



def calc_shear(Pt, xt, Pli, Ple, Pri, Pre, direction, span_begin, span_end):
    """Calculate shear on one side of the node.
   

    Moving left to right:
        Ve1 = abs(Pt*(xt-span_begin)/span_length - Pri)
        Ve2 = abs(Pt*(xt-span_begin)/span_length - Pre)
    Moving right to left
        Ve1 = abs(Pt*(span_end - xt)/span_length - Pli)
        Ve2 = abs(Pt*(span_end - xt)/span_length - Ple)

    Args:
        Rb (float): reaction at beginning of span
        Pr (float): the load on the span to the right of the node
        Pl (float): the load on the span to the left of the node 
        direction (str): flag to determine which direction is being calculated,
                            either 'ltr' or 'rtl'

    Returns:
        Vi (float): shear at analysis node with load included
        Ve (float): shear at analysis node with load excluded

    Notes:
        Calculate shear on both sides of the analysis node, with the load at
        the node included and load excluded.

        Effectively this considers the load at the analysis node to be just
        to the right or left of the analysis node to accurately capture the
        effects of shear on each side of the node.

        The load occuring directly at the analysis node is effectively a
        discontinuity in the shear force. To overcome the discontinuity the
        program looks at the shear force just before and just after the 
        load at the analysis node.
    """
    span_length = span_end - span_begin

    if direction == "ltr":
        Vi = abs(Pt*(xt-span_begin)/span_length - Pri)
        Ve = abs(Pt*(xt-span_begin)/span_length - Pre)
    elif direction == "rtl":
        Vi = abs(Pt*(span_end - xt)/span_length - Pli)
        Ve = abs(Pt*(span_end - xt)/span_length - Ple)

    return round(max(Vi,Ve),3)


def envelope_shear(Ve, V_max, M, M_corr, axle_id, direction, V_max_axle, index_id):
    """Envelope the maximum and minimum shear at each node.
    
    Args:
        Ve (float): shear at analysis node
        V_max (list): maximum shear at each node
        M (float): corresponding moment at analysis node
        M_corr (list): corresponding moment at each node
        index_id (int): analysis node number 
    
    Returns:
        None

    Notes:
        If Ve is greater than the current maxmimum shear at the current
        analysis node the maximum shear is updated as Ve.
    """
    try:
        if V_max[index_id] < Ve:
            V_max[index_id] = Ve
            M_corr[index_id] = M
            V_max_axle[index_id][0] = axle_id
            V_max_axle[index_id][1] = direction
        if V_max[index_id] == Ve and M_corr[index_id] < M:
            M_corr[index_id] = M
            V_max_axle[index_id][0] = axle_id
            V_max_axle[index_id][1] = direction
    except:
        V_max.append(Ve)
        M_corr.append(M)
        V_max_axle.append([axle_id, direction])


def calc_moment(x, xli, xle, xri, xre, span_begin, span_end, Rb, Pli, Ple, Pri, Pre, direction, Pt, xt):
    """Calculate moment at node.

    Moving left to right:
        eli = x - xli
        ele = x - xle
        eb = x - span_begin
        Mi = Rb*eb - Pli*eli
        Me = Rb*eb - Ple*ele
    Moving right to left:
        eri = xri - x
        ere = xre - x
        eb = span_end - x
        Mi = Rb*eb - Pri*eri
        Me = Rb*eb - Pre*ere
    
    Args:
        x (float): x-coordinate of node location
        xli (float): the x-coordinate of the equivalent load to the left of the
                    node including the load at the node
        xle (float): the x-coordinate of the equivalent load to the left of the
                    node excluding the load at the node
        xri (float): the x-coordinate of the equivalent load to the right of the
                    node including the load at the node
        xre (float): the x-coordinate of the equivalent load to the right of the
                    node excluding the load at the node
        span_begin (float): coordinate location of beginning of span
        span_end (float): coordinate location of end of span
        Rb (float): reaction at the beginning of the span
        Pli (float): the load on the span to the left of the node including the
                    load at the node
        Ple (float): the load on the span to the left of the node excluding the
                    load at the node
        Pri (float): the load on the span to the right of the node including the
                    load at the node
        Pre (float): the load on the span to the right of the node excluding the
                    load at the node
        direction (str): flag to determine which direction is being calculated,
                            either 'ltr' or 'rtl'

    Returns:
        M (float): moment at the analysis node for the given span length and
                   axle location

    Notes:
        It shouldn't matter if the point load at the analysis node is included
        or excluded. The moment is being taken about the analysis node so the 
        point load located directly at the analysis node will not produce any
        moment at the analysis node.

        Include both "sides" here for berevity. 
    """
    if direction == "ltr":
        eli = x - xli
        ele = x - xle
        eb = x - span_begin
        Mi = Rb*eb - Pli*eli
        Me = Rb*eb - Ple*ele
    elif direction == "rtl":
        eri = xri - x
        ere = xre - x
        eb = span_end - x
        Mi = Rb*eb - Pri*eri
        Me = Rb*eb - Pre*ere

    return round(max(Mi,Me),3)


def envelope_moment(M, M_max, Ve, V_corr, axle_id, direction, M_max_axle, index_id):
    """Envelope maximum positive moment at each node.

    Args:
        M (float): moment at analysis node
        M_max (list): maximum moment at each node
        Ve (float): corresponding shear at analysis node
        V_corr (list): corresponding shear at each node
        index_id (int): analysis node number 
    
    Returns:
        None

    Notes:
        If M is greater than the current maxmimum moment at the current
        analysis node the maximum moment is updated as M.
    """
    try:
        if M_max[index_id] < M:
            M_max[index_id] = M
            V_corr[index_id] = Ve
            M_max_axle[index_id][0] = axle_id
            M_max_axle[index_id][1] = direction
            #print index_id, M, Ve, M_max[index_id], V_corr[index_id], axle_id, direction
        if M_max[index_id] == M and V_corr[index_id] < Ve:
            V_corr[index_id] = Ve
            M_max_axle[index_id][0] = axle_id
            M_max_axle[index_id][1] = direction
            #print index_id, M, Ve, M_max[index_id], V_corr[index_id], axle_id, direction
    except:
        M_max.append(M)
        V_corr.append(Ve)
        M_max_axle.append([axle_id, direction])
        #print index_id, M, Ve, M_max[index_id], V_corr[index_id], axle_id, direction


def number_axles(num_axles):
    """Numbers the axles starting with 1."""
    axle_num = []

    for i in range(num_axles):
        axle_num.append(i+1)

    return axle_num


def get_abs_axle_location(axle_spacing, start_pt, direction):
    """Calculates the absolute location of the axles wrt the start point."""
    abs_axle_location = []

    loc = start_pt #initialize

    for spacing in axle_spacing:
        if direction == "ltr":
            loc = loc - spacing
        elif direction == "rtl":
            loc = loc + spacing
        abs_axle_location.append(round(loc,3))

    return abs_axle_location          


def move_axle_loc(axle_spacing, axle_id, prev_axle_loc,
                  num_axles, direction):
    """Calculates the current loaction of all the axles on or off the span.

    Steps each axle from its previous location to the current location which
    is determined from the spacing associated with the axle_id axle. 

    Args:
        axle_spacing (list of floats): the spacing between each axle
        axle_id (int): index of axle to placed over the node
        prev_axle_loc (list of floats): x-coordinate of the previous location of
                                        each axle
        num_axles (int): number of program defined axles (includes axles for
                         approximate distributed load)
        direction (str): flag to determine which direction is being calculated,
                            either 'ltr' or 'rtl'

    Returns:
        cur_axle_loc (list of floats): the location of each axle on or off the
                                       span with the axle_id axle located over
                                       the current node 
    """
    cur_axle_loc = []
    
    for i in range(num_axles):
        if direction == "ltr":
            axle_loc = prev_axle_loc[i] + axle_spacing[axle_id-1] 
        elif direction == "rtl":
            axle_loc = prev_axle_loc[i] - axle_spacing[axle_id-1]

        cur_axle_loc.append(round(axle_loc,3))

    return cur_axle_loc
   

def calc_load_and_loc(cur_axle_loc, axle_wt, x, begin_span, end_span, num_axles):
    """Calculate the load and its location on the span.
    
    Calculates the total load and its location on the span, and the load and
    its location to the left and right of the node (critical section) both
    including and excluding the load at the node to capture the effects of the 
    load to either side of the node.
  
    Args:
        cur_axle_loc (list of floats): current x-coordinate of all axles on span
        axle_wt (list of floats): weight of each axle
        x (float): x-coordinate of node location
        begin_span (float): x-coordinate of the beginning of the span
        end_span (float): x-coordinate of the end of the span
        num_axles (int): number of program defined axles (includes axles for
                         approximate distributed load)
   
    Returns:
        Pt (float): total load on the span due to the axles on the span
        xt (float): the x-coordinate of the equivalent total load on the span
        Pli (float): the load on the span to the left of the node *including*
                     the load at the node
        Ple (float): the load on the span to the left of the node *excluding*
                     the load at the node
        xli (float): the x-coordinate of the equivalent load to the left of the
                     node *including* the load at the node
        xlei (float): the x-coordinate of the equivalent load to the left of the
                     node *excluding* the load at the node
        Pri (float): the load on the span to the right of the node *including*
                     the load at the node
        Pre (float): the load on the span to the right of the node *excluding*
                     the load at the node
        xri (float): the x-coordinate of the equivalent load to the right of
                     the node *including* the load at the node
        xre (float): the x-coordinate of the equivalent load to the right of
                     the node *excluding* the load at the node
    """

    Pt = 0.0
    xt = 0.0
    sum_Ptx = 0.0

    Pli = 0.0
    xli = 0.0
    sum_Plix = 0.0

    Ple = 0.0
    xle = 0.0
    sum_Plex = 0.0

    Pri = 0.0
    xri = 0.0
    sum_Prix = 0.0
    
    Pre = 0.0
    xre = 0.0
    sum_Prex = 0.0

    for i in range(num_axles):
        #if the axle is on the span add to total weight on span
        if cur_axle_loc[i] >= begin_span and cur_axle_loc[i] <= end_span:
            Pt = Pt + axle_wt[i]
            sum_Ptx = sum_Ptx + cur_axle_loc[i]*axle_wt[i]
            #if the axle is to the left of the analysis node, add weight to
            #total left of the analysis node
            #point load included
            if cur_axle_loc[i] >= begin_span and cur_axle_loc[i] <= x:
                Pli = Pli + axle_wt[i]
                sum_Plix = sum_Plix + cur_axle_loc[i]*axle_wt[i]
            #point load excluded
            if cur_axle_loc[i] >= begin_span and cur_axle_loc[i] < x:
                Ple = Ple + axle_wt[i]
                sum_Plex = sum_Plex + cur_axle_loc[i]*axle_wt[i]
            #if the axle is to the right of the analysis node, add weight to
            #total right of the analysis node
            #point load included
            if cur_axle_loc[i] >= x and cur_axle_loc[i] <= end_span:
                Pri = Pri + axle_wt[i]
                sum_Prix = sum_Prix + cur_axle_loc[i]*axle_wt[i]
            #point load excluded
            if cur_axle_loc[i] > x and cur_axle_loc[i] <= end_span:
                Pre = Pre + axle_wt[i]
                sum_Prex = sum_Prex + cur_axle_loc[i]*axle_wt[i]
            
    #avoid divide by zero error
    if Pt == 0:
        xt = 0
    else:        
        xt = sum_Ptx/Pt

    if Pli == 0:
        xli = 0
    else:        
        xli = sum_Plix/Pli

    if Ple == 0:
        xle = 0
    else:        
        xle = sum_Plex/Ple

    if Pri == 0:
        xri = 0
    else:        
        xri = sum_Prix/Pri

    if Pre == 0:
        xre = 0
    else:        
        xre = sum_Prex/Pre

    #print Pt
    #print (Pl + Pr)

    return Pt, xt, Pli, Ple, xli, xle, Pri, Pre, xri, xre


def add_trailing_load(axle_spacing, axle_wt, space_to_trailing_load,
        distributed_load, span1_begin, span2_end, pt_load_spacing=0.5):
    """Approximates the distributed trailing load as closely spaced point loads.

    The distributed trailing load is approximated as discretly spaced point
    loads. The point load spacing is assumed to be 0.5 unless the user
    specifically enters a different spacing. The number of loads to add is
    determined by dividing the total span length, span 1 plus span 2, by the
    point load spacing. 
    
    Args:
        axle_spacing (list of floats): spacing of axles used for analysis
        axle_wt (list of floats): weight of axles used for analysis
        space_to_trailing_load (float): distance from last discrete axle to
                                        beginning of distributed load
        distributed_load (float): uniformly distributed trailing load magnitude
        span1_begin (float): coordinate location of beginning of span 1
        span2_end (float): coordinate location of end of span 2
        point_load_spacing (float, optional): spacing of approximate discretely
                                           spaced point loads, defaults to 0.5

    Returns:
        axle_spacing (list of floats): user input axle spacing appended with
                                       axle spacing for discretely spaced loads
                                       to approximate the distributed load
        axle_wt (list of floats): user input axle weights appended with axle
                                       weights for discretely spaced loads to
                                       approximate the distributed load

    Notes:
        Based on testing it can be shown that a reasonable level of accuracy is
        found in the forces and reactions using a discrete point load spacing of
        0.5. This spacing assumes the span lengths are entered in feet.   

        If the user does not want to have a distributed load on the entire
        length of the bridge it is suggested that the actual axle spacing and
        axle weights of the trailing load are entered and no distributed load is
        specified.
        """

    #approximate a distributed trailing load as closely spaced point loads
    #each point load is the distributed load times the point load spacing
    #the point load spacing is a function of the span lenght and number of
    #divisions required
    mod_axle_spacing = axle_spacing[:]
    mod_axle_wt = axle_wt[:]
    
    if space_to_trailing_load < 0.0:
        raise ValueError("Must enter a positive float for space to trialing"
                            "load.")
    elif distributed_load < 0.0:
        raise ValueError("Must enter a positive float for distributed load.")
    elif pt_load_spacing <= 0.0:
        raise ValueError("Must enter a positive float (or nothing for default"
                            "value of 0.5) for the point load spacing.")
    elif distributed_load != 0.0 and space_to_trailing_load != 0.0:
        total_span_length = span2_end - span1_begin
        num_loads = int(total_span_length/pt_load_spacing)
        equivalent_pt_load = distributed_load*pt_load_spacing

        mod_axle_spacing.append(space_to_trailing_load)
        mod_axle_wt.append(equivalent_pt_load)

        for x in range(num_loads):
            mod_axle_spacing.append(pt_load_spacing)
            mod_axle_wt.append(equivalent_pt_load)

    return mod_axle_spacing, mod_axle_wt


def node_location(span1_begin, span1_end, span2_begin, span2_end, num_nodes):
    """Calculate the coordinate location of the analysis nodes.

    Args:
        span1_begin (float): coordinate location of beginning of span 1
        span1_end (float): coordinate location of end of span 1
        span2_begin (float): coordinate location of beginning of span 2
        span2_end (float): coordinate location of end of span 2
        num_nodes (int): number of analysis nodes input by the user

    Returns:
        node_loc (list of floats): list of the coordinate locations of the
                                    analysis nodes along the beam

    Notes:
        The node values are rounded to three (3) decimal places. Otherwise the
        computer rounding messes up the functionality of later functions. For
        example if a node location is supposed to be directly over a pier
        support but it is 0.000000001 off the program will run as if that load
        is acting on span 1 and span 2 won't have that load applied even though
        it should be. 
    """
    span_length1 = span1_end - span1_begin
    span_length2 = span2_end - span2_begin

    if span_length1 < 0.0:
        raise ValueError("Must enter a positive float for span 1 length.")
    elif span_length2 < 0.0:
        raise ValueError("Must enter a positive float for span 2 length (or"
                "nothing for a default value of 0.0).")
    elif num_nodes <= 0:
        raise ValueError("Must enter a postive interger for number of nodes"
                            "(the recommended minimum number of nodes is 21.).")
    else:
        node_loc = []
        
        #span length 1 node locations
        x1 = 0.0
        dx1 = span_length1/(num_nodes - 1)

        for i in range(num_nodes):
            if i == 0:
                node_loc.append(x1)
            elif i == (num_nodes - 1):
                node_loc.append(span1_end)
            else:
                x1 = round(x1 + dx1,3)
                node_loc.append(x1)

        #span length 2 node locations
        if span_length2 > 0:

            x2 = span_length1
            dx2 = span_length2/(num_nodes - 1)
            
            for i in range(num_nodes):
                if i == 0:
                    pass #second span beginning is end of first span
                elif i == (num_nodes - 1):
                    node_loc.append(span2_end)
                else:
                    x2 = round(x2 + dx2,3)
                    node_loc.append(x2)

    return node_loc


def span_begin_end_coords(span_length1, span_length2=0.0):
    """Calculate the span beginning and end coordinates for spans 1 and 2.
    
    Args:
        span_length1 (float): length of span 1
        span_length2 (float, optional): length of span 2

    Returns:
        span1_begin (float): coordinate location of beginning of span 1
        span1_end (float): coordinate location of end of span 1
        span2_begin (float): coordinate location of beginning of span 2
        span2_end (float): coordinate location of end of span 2

        Parameters are returned as a tuple in the following order:
        (span1_begin, span1_end, span2_begin, span2_end)
    """
    if span_length1 < 0.0:
        raise ValueError("Must enter a positive float for span 1 length.")
    elif span_length2 < 0.0:
        raise ValueError("Must enter a positive float for span 2 length (or"
                            "nothing for a default value of 0.0).")
    else:
        span1_begin = 0.0
        span1_end = round(span_length1,3)
        span2_begin = round(span_length1,3)
        span2_end = round(span_length1 + span_length2,3)
        return span1_begin, span1_end, span2_begin, span2_end
