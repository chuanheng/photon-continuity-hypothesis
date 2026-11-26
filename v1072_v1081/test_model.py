import unittest
import numpy as np
from .model import run,blocks,turn,I,X,Y,Z
class Orders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()
    def test_commute(self):
        r=self.r['order_sign'];self.assertAlmostEqual(r['anticommuting'],-1);self.assertEqual(r['same_channel_error'],0)
    def test_finite(self):self.assertAlmostEqual(self.r['finite_rotation']['pminus'],np.sin(.42)**2*np.sin(.56)**2)
    def test_quadrature(self):
        e=self.r['quadrature'];self.assertAlmostEqual(e['eigen_imag'][0]**2+e['real']**2,1)
        self.assertLess(e['eigen_imag'][0]*e['eigen_imag'][1],0)
    def test_record(self):
        e0=np.array([1,0]);e1=np.array([.38,np.sqrt(1-.38**2)])
        self.assertAlmostEqual(np.linalg.norm(e0+e1)**2/4,self.r['order_record']['pminus'])
    def test_unequal(self):self.assertAlmostEqual(self.r['unequal_loss']['unconditional_dark'],.05)
    def test_correlated(self):self.assertAlmostEqual(self.r['channel_memory']['independent'],(10-6)/16);self.assertAlmostEqual(self.r['channel_memory']['shared'],1)
    def test_depol(self):
        d,c=blocks(np.array([I,X,Y,Z])/2,np.array([I,X,Y,Z])/2,(I+Y)/2)
        np.testing.assert_allclose(d,I/2,atol=1e-14);np.testing.assert_allclose(c,(I+Y)/8,atol=1e-14)
    def test_kraus(self):self.assertLess(max(self.r['kraus_gauge'].values()),1e-14)
    def test_offset(self):self.assertAlmostEqual(*self.r['device_phase'].values())
    def test_material(self):self.assertLess(max(self.r['material'].values()),1e-14)
