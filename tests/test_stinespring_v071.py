import unittest,numpy as np
from models.stinespring_v071 import *
class Tests(unittest.TestCase):
 def test_isometry(self):
  for g in np.linspace(0,1,21):self.assertTrue(np.allclose(isometry(g).conj().T@isometry(g),np.eye(2)))
 def test_kraus(self):
  for g in np.linspace(0,1,21):
   r=np.array([[.5,.3j],[-.3j,.5]])
   self.assertTrue(np.allclose(channel_from_isometry(isometry(g),r,2),sum(k@r@k.conj().T for k in kraus(g))))
 def test_rotations(self):
  r=np.array([[.6,.2],[.2,.4]])
  for g in [.0,.1,.4,.9,1.]:
   for p in np.linspace(0,2*np.pi,13):
    self.assertTrue(np.allclose(channel_from_isometry(environment_rotate(isometry(g),phase_unitary(p)),r,2),channel_from_isometry(isometry(g),r,2)))
 def test_rank(self):
  self.assertEqual(choi_rank(0),1)
  for g in [.1,.5,1.]:self.assertEqual(choi_rank(g),2)
 def test_identity_extension(self):
  r=np.array([[.3,.1],[.1,.7]])
  for g in [.1,.5,1.]:
   for a in [np.array([1,0]),np.array([0,1]),np.array([1,1])/np.sqrt(2)]:
    w=extra_identity(isometry(g),a)
    self.assertTrue(np.allclose(w.conj().T@w,np.eye(2)))
    self.assertTrue(np.allclose(channel_from_isometry(w,r,4),channel_from_isometry(isometry(g),r,2)))
 def test_invalid(self):
  with self.assertRaises(ValueError):isometry(-.1)
  with self.assertRaises(ValueError):extra_identity(isometry(.5),[1,1])
if __name__=='__main__':unittest.main()
