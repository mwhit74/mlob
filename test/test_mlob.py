import unittest
from ml import mlob

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
        span1_begin = 0.0
        span2_end = 20.0
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
        span1_begin = 0.0
        span2_end = 70.0
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
        span1_begin = 0.0
        span2_end = 20.0
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

    def test_calc_load_and_loc(self):
