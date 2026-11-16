"""15 small mathematical and archival assertions for the v0.86 audit."""
import unittest
import numpy as np
from pathlib import Path
import json
class OperationalEquivalence(unittest.TestCase):
 def means(self,b,d,u):return 40*(1+.8*np.cos(.18+np.asarray(u)+b+d))+.5
 def test_relabel_gaussian(self):
  u=np.random.default_rng(19).normal(0,.3,100)
  self.assertTrue(np.allclose(self.means(.11,.2,u),self.means(.31,0,u)))
 def test_relabel_random_walk(self):
  u=np.random.default_rng(23).normal(0,.03,300).cumsum()
  self.assertTrue(np.allclose(self.means(.11,.2,u),self.means(.31,0,u)))
 def test_information_rank_one(self):self.assertEqual(np.linalg.matrix_rank(np.ones((2,2))),1)
 def test_information_null(self):self.assertTrue(np.allclose(np.ones((2,2))@np.array([1,-1]),0))
 def test_calibration_lifts_rank(self):
  x=25*np.ones((2,2));x[0,0]+=400
  self.assertEqual(np.linalg.matrix_rank(x),2)
 def test_partial_trace_cannot_access_ancilla(self):
  rho=np.array([[.5,.5j],[-.5j,.5]])
  z0=np.diag([1,0]);z1=np.diag([0,1]);m=np.diag([.7,.3])
  a=np.trace(np.kron(rho,z0)@np.kron(m,np.eye(2)))
  b=np.trace(np.kron(rho,z1)@np.kron(m,np.eye(2)))
  self.assertAlmostEqual(a.real,b.real)
 def test_bosonic_slot(self):
  swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
  p=(np.eye(4)+swap)/2;z=np.diag([1,-1]);i=np.eye(2)
  self.assertTrue(np.allclose(p@np.kron(z,i)@p,p@np.kron(i,z)@p))
 def test_symmetric_internal_states(self):
  a=np.array([1,0]);b=np.array([0,1]);v=(np.kron(a,b)+np.kron(b,a))/np.sqrt(2)
  self.assertTrue(np.allclose(v.reshape(2,2),v.reshape(2,2).T))
class ManifestTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.r=json.loads(Path('results/research_audit_v086.json').read_text())['records']
 def test_36(self):self.assertEqual(len(self.r),36)
 def test_versions(self):self.assertEqual([x['version'] for x in self.r],['v0.'+str(v).zfill(2) for v in range(50,86)])
 def test_passed(self):self.assertEqual(sum(x['unittest_status']=='pass' for x in self.r),34)
 def test_tests(self):self.assertEqual(sum(x['test_count'] or 0 for x in self.r),1086)
 def test_missing(self):self.assertEqual([x['version'] for x in self.r if x['unittest_status']!='pass'],['v0.68','v0.75'])
 def test_51_66(self):self.assertEqual(sum(x['test_count'] or 0 for x in self.r if 51<=int(x['version'].split('.')[1])<=66),666)
 def test_positive_count(self):self.assertTrue(all((x['test_count'] or 0)>0 for x in self.r if x['unittest_status']=='pass'))
if __name__=='__main__':unittest.main()
