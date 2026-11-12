import math, pathlib, sys, unittest
import numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from rabi_observed_spectrum import *
class Tests(unittest.TestCase):
 def setUp(self): self.e,self.s=rabi_levels(6)
 def test_shapes(self): self.assertEqual(self.s.shape,(12,12))
 def test_energies(self): self.assertTrue(np.all(np.diff(self.e)>=0))
 def test_strength_symmetry(self): self.assertTrue(np.allclose(self.s,self.s.T))
 def test_strength_positive(self): self.assertTrue(np.all(self.s>=0))
 def test_bad_cutoff(self):
  with self.assertRaises(ValueError): rabi_levels(1)
 def test_bad_coupling(self):
  with self.assertRaises(ValueError): rabi_levels(coupling=float('nan'))
 def test_ground_population(self): self.assertEqual(np.argmax(thermal_populations(self.e,0)),0)
 def test_ground_normalization(self): self.assertAlmostEqual(thermal_populations(self.e,0).sum(),1)
 def test_thermal_normalization(self): self.assertAlmostEqual(thermal_populations(self.e,.5).sum(),1)
 def test_thermal_positive(self): self.assertTrue(np.all(thermal_populations(self.e,.5)>0))
 def test_negative_temperature(self):
  with self.assertRaises(ValueError): thermal_populations(self.e,-1)
 def test_nan_temperature(self):
  with self.assertRaises(ValueError): thermal_populations(self.e,float('nan'))
 def test_empty_energies(self):
  with self.assertRaises(ValueError): thermal_populations([],1)
 def test_upward_lines(self): self.assertTrue(all(f>0 for f,_ in transitions(self.e,self.s,thermal_populations(self.e,.5))))
 def test_line_weights(self): self.assertTrue(all(w>0 for _,w in transitions(self.e,self.s,thermal_populations(self.e,.5))))
 def test_ground_lines(self): self.assertGreater(len(transitions(self.e,self.s,thermal_populations(self.e,0))),0)
 def test_invalid_population(self):
  with self.assertRaises(ValueError): transitions(self.e,self.s,np.ones(len(self.e)))
 def test_invalid_threshold(self):
  with self.assertRaises(ValueError): transitions(self.e,self.s,thermal_populations(self.e,0),-1)
 def test_lorentz_peak(self): self.assertAlmostEqual(float(lorentzian(1,1,.1)),1/(math.pi*.1))
 def test_lorentz_symmetry(self): self.assertAlmostEqual(float(lorentzian(.8,1,.1)),float(lorentzian(1.2,1,.1)))
 def test_lorentz_invalid(self):
  with self.assertRaises(ValueError): lorentzian(1,1,0)
 def test_voigt_sigma_zero(self): self.assertAlmostEqual(float(voigt_gauss_quadrature(1,1,.1,0)),float(lorentzian(1,1,.1)))
 def test_voigt_positive(self): self.assertGreater(float(voigt_gauss_quadrature(1,1,.1,.1)),0)
 def test_voigt_symmetry(self): self.assertAlmostEqual(float(voigt_gauss_quadrature(.8,1,.1,.1)),float(voigt_gauss_quadrature(1.2,1,.1,.1)))
 def test_voigt_invalid_sigma(self):
  with self.assertRaises(ValueError): voigt_gauss_quadrature(1,1,.1,-.1)
 def test_voigt_invalid_order(self):
  with self.assertRaises(ValueError): voigt_gauss_quadrature(1,1,.1,.1,3)
 def test_empty_lines(self): self.assertTrue(np.all(observed_spectrum([1,2],[])==0))
 def test_spectrum_positive(self): self.assertTrue(np.all(observed_spectrum(np.linspace(0,2,20),[(1,1)])>0))
 def test_spectrum_linear(self):
  x=np.linspace(0,2,20);self.assertTrue(np.allclose(observed_spectrum(x,[(1,2)]),2*observed_spectrum(x,[(1,1)])))
 def test_invalid_line(self):
  with self.assertRaises(ValueError): observed_spectrum([1],[(1,-1)])
 def test_invalid_grid(self):
  with self.assertRaises(ValueError): observed_spectrum([float('nan')],[(1,1)])
 def test_finite_output(self): self.assertTrue(np.all(np.isfinite(observed_spectrum(np.linspace(0,2,20),[(1,1)]))))
 def test_low_temp(self): self.assertGreater(thermal_populations(self.e,.1)[0],thermal_populations(self.e,1)[0])
 def test_vector_voigt(self): self.assertEqual(voigt_gauss_quadrature(np.array([0.,1.]),1,.1,.1).shape,(2,))
 def test_zero_coupling(self): self.assertAlmostEqual(rabi_levels(4,coupling=0)[0][0],-.5)
if __name__=='__main__': unittest.main()
