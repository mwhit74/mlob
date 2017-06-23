import unittest
from ml import mlob
import pdb

class TestUserInput(unittest.TestCase):
    
    def setUp(self):
        pass
    def tearDown(self):
        pass 
    def test_get_axle_spacing(self):
        pass
    def test_get_axle_wt(self):
        pass
    def test_space_to_trailing_load(self):
        pass
    def test_distributed_load(self):
        pass
    def test_span1_length(self):
        pass
    def test_span2_length(self):
        pass
    def test_num_analysis_nodes(self):
        pass

class TestMlob(unittest.TestCase):


    def setUp(self):
        self.axle_spacing_E80 = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00,
                                 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00,
                                 5.00, 6.00, 5.00]
        self.axle_wt_E80 = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00,
                            52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00,
                            52.00, 52.00, 52.00, 52.00]
        self.axle_spacing_286k = [3.042,5.83,21.5,5.83,3.042]
        self.axle_wt_286k = [71.50,71.50,71.50,71.50]
        #ul = unit load
        self.axle_spacing_ul = [0.0]
        self.axle_wt_ul = [1.0]

        self.span_0 = 0.0
        self.span_20 = 20.0
        self.span_25 = 25.0
        self.span_50 = 50.0
        self.span_100 = 100.0

        self.num_user_nodes_5 = 5
        self.num_user_nodes_20 = 20
        self.num_user_nodes_50 = 50

        self.space_to_trailing_load_E80 = 5.0
        self.space_to_trailing_load_286k = 0.0
        self.space_to_trailing_load_ul = 0.0

        self.distributed_load_E80 = 8.0
        self.distributed_load_286k = 0.0
        self.distributed_load_ul = 0.0


    def tearDown(self):
        pass


    def test_node_location_l25_n20(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_25, self.span_0)
        
        node_loc = mlob.node_location(span1_begin,
                                         span1_end,
                                         span2_begin,
                                         span2_end,
                                         self.num_user_nodes_20)

        correct_node_loc = [0.0,
                            1.316,
                            2.632,
                            3.948,
                            5.264,
                            6.58,
                            7.896,
                            9.212,
                            10.528,
                            11.844,
                            13.16,
                            14.476,
                            15.792,
                            17.108,
                            18.424,
                            19.74,
                            21.056,
                            22.372,
                            23.688,
                            25.004]
        err_str = ""
        for nl, cnl in zip(node_loc, correct_node_loc):
            if cnl == 0.0:
                self.assertTrue(nl == cnl)
            else:
                error = abs((cnl-nl)/cnl)
                msg = str(nl) + " : " + str(cnl) + " : " + str(error)
                self.assertAlmostEqual(nl, cnl, places=2, msg=msg)


    def test_span_begin_end_coords_l1pos_l2(self):
        #also checks that span length 2 defaults to 0.0
        func_tuple = mlob.span_begin_end_coords(self.span_25)
        correct_tuple = (0.0,25.0,25.0,25.0)
        self.assertEqual(func_tuple, correct_tuple)
    

    def test_span_begin_end_coords_l1pos_l2pos(self):
        func_tuple = mlob.span_begin_end_coords(self.span_50, self.span_25)
        correct_tuple = (0.0,50.0,50.0,75.0)
        self.assertEqual(func_tuple, correct_tuple)


    def test_span_begin_end_coords_l1neg_l2(self):
        self.assertRaises(ValueError, mlob.span_begin_end_coords,
                -1*self.span_50)


    def test_span_begin_end_coords_l1pos_l2neg(self):
        self.assertRaises(ValueError, mlob.span_begin_end_coords,
                self.span_50, -1*self.span_25)


    def test_add_trailing_load_single_span_e80(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_20)
        mlob.add_trailing_load(self.axle_spacing_E80,
                          self.axle_wt_E80,
                          self.space_to_trailing_load_E80,
                          self.distributed_load_E80,
                          span1_begin,
                          span2_end)

        caxle_spacing = [8.0,5.0,5.0,5.0,9.0,5.0,6.0,5.0,8.0,
                         8.0,5.0,5.0,5.0,9.0,5.0,6.0,5.0,5.0,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

        caxle_wt = [40.0,80.0,80.0,80.0,80.0,52.0,52.0,52.0,52.0,
                    40.0,80.0,80.0,80.0,80.0,52.0,52.0,52.0,52.0, 2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]

        for cas, caw, uas, uaw in zip(caxle_spacing, 
                                      caxle_wt,
                                      self.axle_spacing_E80,
                                      self.axle_wt_E80):
            self.assertAlmostEqual(cas, uas, places=3)
            self.assertAlmostEqual(cas, uas, places=3)


    def test_add_trailing_load_two_span_e80(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_20, self.span_50)
        mlob.add_trailing_load(self.axle_spacing_E80,
                          self.axle_wt_E80,
                          self.space_to_trailing_load_E80,
                          self.distributed_load_E80,
                          span1_begin,
                          span2_end)

        caxle_spacing = [8.0,5.0,5.0,5.0,9.0,5.0,6.0,5.0,8.0,
                         8.0,5.0,5.0,5.0,9.0,5.0,6.0,5.0,5.0,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,
                         0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5]

        caxle_wt = [40.0,80.0,80.0,80.0,80.0,52.0,52.0,52.0,52.0,
                    40.0,80.0,80.0,80.0,80.0,52.0,52.0,52.0,52.0, 2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,
                    2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]

        for cas, caw, uas, uaw in zip(caxle_spacing, 
                                      caxle_wt,
                                      self.axle_spacing_E80,
                                      self.axle_wt_E80):
            self.assertAlmostEqual(cas, uas, places=3)
            self.assertAlmostEqual(cas, uas, places=3)


    def test_add_trailing_load_single_span_none(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_20)
        mlob.add_trailing_load(self.axle_spacing_286k,
                          self.axle_wt_286k,
                          self.space_to_trailing_load_286k,
                          self.distributed_load_286k,
                          span1_begin,
                          span2_end)

        caxle_spacing = [3.042,5.83,21.50,5.83,3.042]

        caxle_wt = [71.50,71.50,71.50,71.50]

        for cas, caw, uas, uaw in zip(caxle_spacing, 
                                      caxle_wt,
                                      self.axle_spacing_286k,
                                      self.axle_wt_286k):
            self.assertAlmostEqual(cas, uas, places=3)
            self.assertAlmostEqual(cas, uas, places=3)


    def test_number_axles_E80_l25(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_25)
        mlob.add_trailing_load(self.axle_spacing_E80,
                          self.axle_wt_E80,
                          self.space_to_trailing_load_E80,
                          self.distributed_load_E80,
                          span1_begin,
                          span2_end)
        num_axles = len(self.axle_wt_E80)

        c_axle_num = [1,2,3,4,5,6,7,8,9,10,
                      11,12,13,14,15,16,17,18,19,20,
                      21,22,23,24,25,26,27,28,29,30,
                      31,32,33]

        axle_num = mlob.number_axles(num_axles)

        for c_num, num in zip(c_axle_num, axle_num):
            self.assertEqual(c_num, num)


    def test_number_axles_E80_l20_l50(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_20, self.span_50)
        mlob.add_trailing_load(self.axle_spacing_E80,
                          self.axle_wt_E80,
                          self.space_to_trailing_load_E80,
                          self.distributed_load_E80,
                          span1_begin,
                          span2_end)
        num_axles = len(self.axle_wt_E80)

        c_axle_num = [1,2,3,4,5,6,7,8,9,10,
                      11,12,13,14,15,16,17,18,19,20,
                      21,22,23,24,25,26,27,28,29,30,
                      31,32,33,34,35,36,37,38,39,40,
                      41,42,43,44,45,46,47,48,49,50,
                      51,52,53,54,55]

        axle_num = mlob.number_axles(num_axles)

        for c_num, num in zip(c_axle_num, axle_num):
            self.assertEqual(c_num, num)


    def test_number_axles_286k_l50(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_20)
        mlob.add_trailing_load(self.axle_spacing_286k,
                          self.axle_wt_286k,
                          self.space_to_trailing_load_286k,
                          self.distributed_load_286k,
                          span1_begin,
                          span2_end)
        num_axles = len(self.axle_wt_286k)

        c_axle_num = [1,2,3,4]

        axle_num = mlob.number_axles(num_axles)

        for c_num, num in zip(c_axle_num, axle_num):
            self.assertEqual(c_num, num)

    
    def test_move_axle_loc_E80_ltr_x0(self):
        self.axle_spacing_E80.insert(0, 0.0)
        x = 0.0 #node location
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80, 
                                                   x, "ltr")
        num_axles = len(self.axle_wt_E80)

        cur_axle_loc = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "ltr")

        c_cur_axle_loc = [8.0, 0.0, -5.0, -10.0,
                          -15.0, -24.0, -29.0, -35.0,
                          -40.0, -48.0, -56.0, -61.0,
                          -66.0, -71.0, -80.0, -85.0,
                          -91.0, -96.0]

        for loc, c_loc in zip(cur_axle_loc, c_cur_axle_loc):
            self.assertAlmostEqual(loc, c_loc, places=3)


    def test_move_axle_loc_E80_rtl_x20(self):
        self.axle_spacing_E80.insert(0, 0.0)
        x = 20.0 #node location
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80, 
                                                   x, "rtl")
        num_axles = len(self.axle_wt_E80)

        cur_axle_loc = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "rtl")

        c_cur_axle_loc = [12.0, 20.0, 25.0, 30.0, 
                          35.0, 44.0, 49.0, 55.0, 
                          60.0, 68.0, 76.0, 81.0, 
                          86.0, 91.0, 100.0, 105.0,
                          111.0, 116.0]

        for loc, c_loc in zip(cur_axle_loc, c_cur_axle_loc):
            self.assertAlmostEqual(loc, c_loc, places=3)


    def test_calc_load_and_loc_E80_ltr_x75_l100_aid1(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        cur_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "ltr")
        Pt, xt, Pl, xl, Pr, xr = mlob.calc_load_and_loc(cur_axle_loc,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)
        c_Pt = 848.0 
        c_xt = 37.1698
        c_Pl = 848.0
        c_xl = 37.1698
        c_Pr = 40.0
        c_xr = 75.0

        self.assertAlmostEqual(Pt, c_Pt, places=3)
        self.assertAlmostEqual(xt, c_xt, places=3)
        self.assertAlmostEqual(Pl, c_Pl, places=3)
        self.assertAlmostEqual(xl, c_xl, places=3)
        self.assertAlmostEqual(Pr, c_Pr, places=3)
        self.assertAlmostEqual(xr, c_xr, places=3)


    def test_calc_load_and_loc_E80_ltr_x75_l100_aid5(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "ltr")
        cur_axle_loc_2 = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "ltr")
        cur_axle_loc_3 = mlob.move_axle_loc(self.axle_spacing_E80, 3,
                                          cur_axle_loc_2, num_axles, "ltr")
        cur_axle_loc_4 = mlob.move_axle_loc(self.axle_spacing_E80, 4,
                                          cur_axle_loc_3, num_axles, "ltr")
        cur_axle_loc_5 = mlob.move_axle_loc(self.axle_spacing_E80, 5,
                                          cur_axle_loc_4, num_axles, "ltr")
        Pt, xt, Pl, xl, Pr, xr = mlob.calc_load_and_loc(cur_axle_loc_5,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)
        c_Pt = 1032.0
        c_xt = 51.6705
        c_Pl = 752.0
        c_xl = 38.5691
        c_Pr = 360.0
        c_xr = 84.2222

        self.assertAlmostEqual(Pt, c_Pt, places=3)
        self.assertAlmostEqual(xt, c_xt, places=3)
        self.assertAlmostEqual(Pl, c_Pl, places=3)
        self.assertAlmostEqual(xl, c_xl, places=3)
        self.assertAlmostEqual(Pr, c_Pr, places=3)
        self.assertAlmostEqual(xr, c_xr, places=3)


    def test_calc_load_and_loc_E80_rtl_x75_l100_aid5(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "rtl")
        cur_axle_loc_2 = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "rtl")
        cur_axle_loc_3 = mlob.move_axle_loc(self.axle_spacing_E80, 3,
                                          cur_axle_loc_2, num_axles, "rtl")
        cur_axle_loc_4 = mlob.move_axle_loc(self.axle_spacing_E80, 4,
                                          cur_axle_loc_3, num_axles, "rtl")
        cur_axle_loc_5 = mlob.move_axle_loc(self.axle_spacing_E80, 5,
                                          cur_axle_loc_4, num_axles, "rtl")
        Pt, xt, Pl, xl, Pr, xr = mlob.calc_load_and_loc(cur_axle_loc_5,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)
        c_Pt = 568.0
        c_xt = 75.3803
        c_Pl = 360.0
        c_xl = 65.7778
        c_Pr = 288.0
        c_xr = 87.2778

        self.assertAlmostEqual(Pt, c_Pt, places=3)
        self.assertAlmostEqual(xt, c_xt, places=3)
        self.assertAlmostEqual(Pl, c_Pl, places=3)
        self.assertAlmostEqual(xl, c_xl, places=3)
        self.assertAlmostEqual(Pr, c_Pr, places=3)
        self.assertAlmostEqual(xr, c_xr, places=3)


    def test_calc_pier_reactions_E80_rtl_x75_l100_aid10(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100, self.span_50)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "rtl")
        cur_axle_loc_2 = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "rtl")
        cur_axle_loc_3 = mlob.move_axle_loc(self.axle_spacing_E80, 3,
                                          cur_axle_loc_2, num_axles, "rtl")
        cur_axle_loc_4 = mlob.move_axle_loc(self.axle_spacing_E80, 4,
                                          cur_axle_loc_3, num_axles, "rtl")
        cur_axle_loc_5 = mlob.move_axle_loc(self.axle_spacing_E80, 5,
                                          cur_axle_loc_4, num_axles, "rtl")
        cur_axle_loc_6 = mlob.move_axle_loc(self.axle_spacing_E80, 6,
                                          cur_axle_loc_5, num_axles, "rtl")
        cur_axle_loc_7 = mlob.move_axle_loc(self.axle_spacing_E80, 7,
                                          cur_axle_loc_6, num_axles, "rtl")
        cur_axle_loc_8 = mlob.move_axle_loc(self.axle_spacing_E80, 8,
                                          cur_axle_loc_7, num_axles, "rtl")
        cur_axle_loc_9 = mlob.move_axle_loc(self.axle_spacing_E80, 9,
                                          cur_axle_loc_8, num_axles, "rtl")
        cur_axle_loc_10 = mlob.move_axle_loc(self.axle_spacing_E80, 10,
                                          cur_axle_loc_9, num_axles, "rtl")
        Pt1, xt1, Pl1, xl1, Pr1, xr1 = mlob.calc_load_and_loc(cur_axle_loc_10,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)
        Pt2, xt2, Pl2, xl2, Pr2, xr2 = mlob.calc_load_and_loc(cur_axle_loc_10,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span2_begin,
                                                        span2_end,
                                                        num_axles)

        c_Rpier = 705.9199 

        Rpier = mlob.calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin,
                span1_end, span2_begin, span2_end)

        self.assertAlmostEqual(c_Rpier, Rpier, places=3)
        

    def test_calc_pier_reactions_E80_ltr_x75_l100_aid10(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100, self.span_50)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "ltr")
        cur_axle_loc_2 = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "ltr")
        cur_axle_loc_3 = mlob.move_axle_loc(self.axle_spacing_E80, 3,
                                          cur_axle_loc_2, num_axles, "ltr")
        cur_axle_loc_4 = mlob.move_axle_loc(self.axle_spacing_E80, 4,
                                          cur_axle_loc_3, num_axles, "ltr")
        cur_axle_loc_5 = mlob.move_axle_loc(self.axle_spacing_E80, 5,
                                          cur_axle_loc_4, num_axles, "ltr")
        cur_axle_loc_6 = mlob.move_axle_loc(self.axle_spacing_E80, 6,
                                          cur_axle_loc_5, num_axles, "ltr")
        cur_axle_loc_7 = mlob.move_axle_loc(self.axle_spacing_E80, 7,
                                          cur_axle_loc_6, num_axles, "ltr")
        cur_axle_loc_8 = mlob.move_axle_loc(self.axle_spacing_E80, 8,
                                          cur_axle_loc_7, num_axles, "ltr")
        cur_axle_loc_9 = mlob.move_axle_loc(self.axle_spacing_E80, 9,
                                          cur_axle_loc_8, num_axles, "ltr")
        cur_axle_loc_10 = mlob.move_axle_loc(self.axle_spacing_E80, 10,
                                          cur_axle_loc_9, num_axles, "ltr")
        Pt1, xt1, Pl1, xl1, Pr1, xr1 = mlob.calc_load_and_loc(cur_axle_loc_10,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)
        Pt2, xt2, Pl2, xl2, Pr2, xr2 = mlob.calc_load_and_loc(cur_axle_loc_10,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span2_begin,
                                                        span2_end,
                                                        num_axles)
        c_Rpier = 718.48

        Rpier = mlob.calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin,
                span1_end, span2_begin, span2_end)

        self.assertAlmostEqual(c_Rpier, Rpier, places=3)


    def test_calc_pier_reactions_E80_ltr_x75_l100_aid5(self):
        (span1_begin,
        span1_end,
        span2_begin,
        span2_end) = mlob.span_begin_end_coords(self.span_100, self.span_50)
        self.axle_spacing_E80.insert(0, 0.0)
        num_axles = len(self.axle_wt_E80)
        x = 75.0
        prev_axle_loc = mlob.get_abs_axle_location(self.axle_spacing_E80,
                                                       x, "ltr")
        cur_axle_loc_2 = mlob.move_axle_loc(self.axle_spacing_E80, 2,
                                          prev_axle_loc, num_axles, "ltr")
        cur_axle_loc_3 = mlob.move_axle_loc(self.axle_spacing_E80, 3,
                                          cur_axle_loc_2, num_axles, "ltr")
        cur_axle_loc_4 = mlob.move_axle_loc(self.axle_spacing_E80, 4,
                                          cur_axle_loc_3, num_axles, "ltr")
        cur_axle_loc_5 = mlob.move_axle_loc(self.axle_spacing_E80, 5,
                                          cur_axle_loc_4, num_axles, "ltr")
        Pt1, xt1, Pl1, xl1, Pr1, xr1 = mlob.calc_load_and_loc(cur_axle_loc_5,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span1_begin,
                                                        span1_end,
                                                        num_axles)

        Pt2, xt2, Pl2, xl2, Pr2, xr2 = mlob.calc_load_and_loc(cur_axle_loc_5,
                                                        self.axle_wt_E80,
                                                        x,
                                                        span2_begin,
                                                        span2_end,
                                                        num_axles)
        c_Rpier = 533.2396

        Rpier = mlob.calc_pier_reaction(Pt1, xt1, Pt2, xt2, span1_begin,
                span1_end, span2_begin, span2_end)

        self.assertAlmostEqual(c_Rpier, Rpier, places=3)
