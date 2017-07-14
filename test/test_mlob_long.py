import unittest
from ml import mlob
import pdb
import timeit

class TestMlobLong(unittest.TestCase):

    def setUp(self):
        self.axle_spacing = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00,
                                 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00,
                                 5.00, 6.00, 5.00]
        self.axle_wt = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00,
                            52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00,
                            52.00, 52.00, 52.00, 52.00]
        self.space_to_trailing_load = 5.0
        self.distributed_load = 8.0

    def test_long(self):
        span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
                        18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
                        60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
                        200.0,250.0,300.0,350.0,400.0]

        num_user_nodes = 21

        header = "{0} {1} {2} {3} {4} {5} {6}".format("Span Length [ft]",
                                                "Max Moment [ft-kips]",
                                                "Max Moment at 1/4 Pt [ft-kips]",
                                                "Max Shear at End [kips]",
                                                "Max Shear at 1/4 Pt [kips]",
                                                "Max Shear at Center [kips]",
                                                "Max Pier Reactions [kips]")
        print header
                                         
        start = timeit.default_timer()
        for span_length in span_lengths:
            node_loc, V_max1, M_max1, V_max2, M_max2, Rmax_pier,\
            span1_begin, span2_begin = mlob.analyze_vehicle(self.axle_spacing,
                                                            self.axle_wt,
                                                            span_length,
                                                            span_length,
                                                            num_user_nodes,
                                                            self.space_to_trailing_load,
                                                            self.distributed_load)
            max_moment = max(M_max1)/2
            max_moment_q = M_max1[5]/2
            max_shear_e = V_max1[0]/2
            max_shear_q = V_max1[5]/2
            max_shear_c = V_max1[10]/2
            r_max_pier = Rmax_pier/2

            out = "{0:^20.3f} {1:^20.3f} {2:^20.3f} {3:^20.3f} {4:^20.3f} {5:^20.3f} {6:^20.3f}".format(span_length,
                                                 max_moment,
                                                 max_moment_q,
                                                 max_shear_e,
                                                 max_shear_q,
                                                 max_shear_c,
                                                 r_max_pier)

            print out
        end = timeit.default_timer()

        print end - start

