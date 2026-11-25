import unittest
import math
from .model import run
from v752_v761.response import compute
a=list(run().values())
fine=compute(3,4001)

class Response(unittest.TestCase):
    def test_782(self):
        self.assertTrue(a[0]["span"] >= max(a[0]["end_ratio"],1/a[0]["end_ratio"])-1e-10)

    def test_783(self):
        self.assertTrue(0 < a[1]["flat_acceptance"] <= 1)

    def test_784(self):
        self.assertTrue(abs(a[2]["original"]-1.345541)<1e-5)

    def test_785(self):
        self.assertTrue(abs(math.log(a[3]["inverse_weighted"]/a[2]["original"])) <= a[6]["bound"]+1e-12)

    def test_786(self):
        self.assertTrue(abs(a[4]["low_line"]/a[4]["high_line"]-a[2]["weighted"]/a[2]["original"])<1e-10)

    def test_787(self):
        self.assertTrue(abs(a[5]["derivative"]-a[5]["finite_difference"])<1e-7)

    def test_788(self):
        self.assertTrue(a[6]["actual"] <= a[6]["bound"]+1e-12)

    def test_789(self):
        self.assertTrue(a[7]["incident_per_endpoint"] >= 800)

    def test_790(self):
        self.assertTrue(abs(a[8]["narrow_log_shift"]-fine[8]["narrow_log_shift"]) < 1e-5)

    def test_791(self):
        self.assertTrue(abs(a[9]["midpoint_relative_residual"]-fine[9]["midpoint_relative_residual"])<1e-8)
