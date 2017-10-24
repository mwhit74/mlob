import unittest
from ml import mlob
import pdb
import timeit

class TestMlobLong(unittest.TestCase):

    def setUp(self):
        self.span_lengths = [5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,16.0,
                        18.0,20.0,24.0,28.0,32.0,36.0,40.0,45.0,50.0,55.0,
                        60.0,70.0,80.0,90.0,100.0,120.0,140.0,160.0,180.0,
                        200.0,250.0,300.0,350.0,400.0]

        self.axle_spacing_e80 = [8.00, 5.00, 5.00, 5.00, 9.00, 5.00, 6.00,
                                 5.00, 8.00, 8.00, 5.00, 5.00, 5.00, 9.00,
                                 5.00, 6.00, 5.00]
        self.axle_wt_e80 = [40.00, 80.00, 80.00, 80.00, 80.00, 52.00, 52.00,
                            52.00, 52.00, 40.00, 80.00, 80.00, 80.00, 80.00,
                            52.00, 52.00, 52.00, 52.00]
        self.space_to_trailing_load_e80 = 5.0
        self.distributed_load_e80 = 8.0

        self.axle_spacing_alt = [5.00, 6.00, 5.00]
        self.axle_wt_alt = [100.00, 100.00, 100.00, 100.00]
        self.space_to_trailing_load_alt = 0.0
        self.distributed_load_alt = 8.0

        self.max_moment_e80 = [50.00,60.00,70.00,80.00,93.89,112.50,
                               131.36,160.00,190.00,220.00,280.00,
                               340.00,412.50,570.42,730.98,910.85,
                               1097.30,1311.30,1601.20,1901.80,2233.10,
                               2597.80,3415.00,4318.90,5339.10,6446.30,
                               9225.40,12406.00,15908.00,19672.00,23712.00,
                               35118.00,48800.00,65050.00,83800.00]
        self.max_moment_alt = [62.50,75.00,87.50,100.00,117.36,140.63,
                               164.20,188.02,212.83,250.30,325.27,400.24,
                               475.00,668.75,866.07,1064.06,1262.50,1461.25,
                               1710.00,1959.00]
        self.max_moment_qtr_pt_e80 = [37.50,45.00,55.00,70.00,85.00,100.00,
                                      115.00,130.00,145.00,165.00,210.00,
                                      255.00,300.00,420.00,555.00,692.50,
                                      851.50,1010.50,1233.60,1473.00,1732.30,
                                      2010.00,2608.20,3298.00,4158.00,5060.50,
                                      7098.00,9400.00,11932.00,14820.00,
                                      17990.00,27154.00,38246.00,51114.00,
                                      65588.00]
        self.max_moment_qtr_pt_alt = [46.88,56.25,68.75,87.50,106.25,125.00,
                                      143.75,162.50,181.25,200.00,250.00,
                                      318.79,362.50,500.00,650.00,800.00,
                                      950.00,1100.00,1287.48,1481.05]
        self.max_shear_end_e80 = [40.00,46.67,51.43,55.00,57.58,60.00,65.45,
                                  70.00,73.84,77.14,85.00,93.33,100.00,110.83,
                                  120.86,131.44,141.12,150.80,163.38,174.40,
                                  185.31,196.00,221.04,248.40,274.46,300.00,
                                  347.35,392.59,436.51,479.57,522.01,626.41,
                                  729.34,831.43,933.00]
        self.max_shear_end_alt = [50.00,58.33,64.29,68.75,72.22,75.00,77.27,
                                  83.33,88.46,92.86,100.00,111.11,120.00,
                                  133.33,142.86,150.00,155.56,160.00,164.44]
        self.max_shear_qtr_pt_e80 = [None,30.00,31.43,35.00,37.78,40.00,
                                     41.82,43.33,44.61,47.14,52.50,56.67,
                                     60.00,70.00,77.14,83.12,88.90,93.55,
                                     100.27,106.97,113.58,120.21,131.89,
                                     143.41,157.47,173.12,202.19,230.23,
                                     265.51,281.96,306.81,367.30,426.37,
                                     484.67,542.40]
        self.max_shear_qtr_pt_alt = [None,37.50,39.29,43.75,47.23,50.00,
                                     52.28,54.17,55.76,57.14,62.50,68.05,
                                     72.50,83.33,92.86,100.00,105.56,
                                     110.00,114.45,118.42,120.91,123.33]
        self.max_shear_ctr_e80 = [20.00,20.00,20.00,20.00,20.00,20.00,
                                  21.82,23.33,24.61,25.71,27.50,28.89,
                                  28.70,31.75,34.29,37.50,41.10,44.00,
                                  45.90,49.73,52.74,55.69,61.45,67.41,
                                  73.48,78.72,88.92,101.64,115.20,128.12,
                                  140.80,170.05,197.93,225.51,252.44]
        self.max_shear_ctr_alt = [25.00,25.00,25.00,25.00,25.00,25.00,
                                  27.28,29.17,30.76,32.14,34.38,36.11,
                                  37.50,41.67,46.43,50.00,55.56,60.00,
                                  64.45,68.00,70.91,73.33,77.14,80.00,
                                  82.22,84.00]
        self.max_pier_reac_e80 = [40.00,53.33,62.86,70.00,75.76,80.00,
                                  87.28,93.33,98.46,104.29,113.74,121.33,
                                  131.10,147.92,164.58,181.94,199.06,
                                  215.90,237.25,257.52,280.67,306.42,
                                  354.08,397.70,437.15,474.24,544.14,
                                  614.91,687.50,762.22,838.00,1030.40,
                                  1225.30,1421.70,1619.00]
        self.max_pier_reac_alt = [50.00,58.33,71.43,81.25,88.89,95.00,
                                  100.00,108.33,115.39,121.43,131.25,
                                  138.89,145.00,154.17]


    def test_e80(self):
        num_user_nodes = 21
        self.run_vehicle(self.axle_spacing_e80,
                    self.axle_wt_e80,
                    num_user_nodes,
                    self.space_to_trailing_load_e80,
                    self.distributed_load_e80,
                    self.max_moment_e80,
                    self.max_moment_qtr_pt_e80,
                    self.max_shear_end_e80,
                    self.max_shear_qtr_pt_e80,
                    self.max_shear_ctr_e80,
                    self.max_pier_reac_e80)

    
    def test_alt(self):
        num_user_nodes = 21
        self.run_vehicle(self.axle_spacing_alt,
                    self.axle_wt_alt,
                    num_user_nodes,
                    self.space_to_trailing_load_alt,
                    self.distributed_load_alt,
                    self.max_moment_alt,
                    self.max_moment_qtr_pt_alt,
                    self.max_shear_end_alt,
                    self.max_shear_qtr_pt_alt,
                    self.max_shear_ctr_alt,
                    self.max_pier_reac_alt)


    def run_vehicle(self, axle_spacing, axle_wt, num_user_nodes, space_to_trailing_load,
            distributed_load, cl_max_moment, cl_max_moment_qtr_pt, cl_max_shear_end,
            cl_max_shear_qtr_pt, cl_max_shear_ctr, cl_max_pier_reac):

                                         
        for i in range(len(self.span_lengths)):
            span_length = self.span_lengths[i]
            (node_loc, V_max1, M_corr1, M_max1, V_corr1,
            V_max2, M_corr2, M_max2, V_corr2, Rmax_pier,
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

            try:
                c_max_moment = cl_max_moment[i]
                e = self.error(c_max_moment, max_moment)
                msg = "Max Moment " + str(c_max_moment) + " " + str(max_moment)
                self.assertLessEqual(e, 0.04,msg)
            except IndexError as e:
                pass

            try:
                c_max_moment_q = cl_max_moment_qtr_pt[i]
                e = self.error(c_max_moment_q, max_moment_q)
                msg = ("Max Moment Qtr Pt " + str(c_max_moment_q) + " " +
                str(max_moment_q))
                self.assertLessEqual(e, 0.04, msg)
            except IndexError as e:
                pass

            try:
                c_max_shear_e = cl_max_shear_end[i]
                e = self.error(c_max_shear_e, max_shear_e)
                msg = ("Max Shear End " + str(c_max_shear_e) + " " +
                str(max_shear_e))
                self.assertLessEqual(e, 0.04, msg)
            except IndexError as e:
                pass

            try:
                c_max_shear_q = cl_max_shear_qtr_pt[i]
                if c_max_shear_q == None:
                    pass
                else:
                    e = self.error(c_max_shear_q, max_shear_q)
                    msg = ("Max Shear Qtr Pt " + str(c_max_shear_q) + " " +
                            str(max_shear_q))
                    self.assertLessEqual(e, 0.04, msg)
            except IndexError as e:
                pass

            try:
                c_max_shear_c = cl_max_shear_ctr[i]
                e = self.error(c_max_shear_c, max_shear_c)
                msg = ("Max Shear Ctr " + str(c_max_shear_c) + " " +
                str(max_shear_c))
                self.assertLessEqual(e, 0.04, msg)
            except IndexError as e:
                pass

            try:
                c_r_max_pier = cl_max_pier_reac[i]
                e = self.error(c_r_max_pier, r_max_pier)
                msg = ("Max Pier Reac " + str(c_r_max_pier) + " " +
                str(r_max_pier))
                self.assertLessEqual(e, 0.04, msg)
            except IndexError as e:
                pass


    def error(self, v1, v2):

        e = abs(v1 - v2)/v1
        return e
