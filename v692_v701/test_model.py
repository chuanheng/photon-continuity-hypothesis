import unittest
import numpy as np
from .model import weights,run

class CommonBand(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run()

    def test_display(self):
        self.assertEqual(self.r['v6.92']['55.791/D2'],100)

    def test_average(self):
        for w in self.r['v6.93'].values():
            self.assertAlmostEqual(sum(w),1)
            self.assertGreaterEqual(min(w),0)
        x=np.array([2.,3.,5.])
        self.assertAlmostEqual(weights(x,(2.5,4.5))@x,3.5)

    def test_physical_units(self):
        self.assertAlmostEqual(self.r['v6.94']['54.612/D1'],0.55733,4)

    def test_common_model(self):
        self.assertEqual(self.r['v6.95']['54.612/D1'],self.r['v6.95']['54.612/D2'])

    def test_distances(self):
        for key,pair in self.r['v6.96'].items():
            self.assertEqual(np.argmin(pair),int(key=='54.612/D2'))

    def test_geometric(self):
        for key,gm in self.r['v6.97'].items():
            self.assertLessEqual(gm,self.r['v6.94'][key])

    def test_error_units(self):
        self.assertAlmostEqual(self.r['v6.98']['55.791/D1'],.08314,4)

    def test_correlation(self):
        for key,sd in self.r['v6.99'].items():
            self.assertGreater(sd,self.r['v6.98'][key])

    def test_window(self):
        for key,pair in self.r['v7.00'].items():
            self.assertEqual(np.argmin(pair),np.argmin(self.r['v6.96'][key]))

    def test_ratio(self):
        self.assertAlmostEqual(self.r['v7.01']['55.791'],1.4076,4)
