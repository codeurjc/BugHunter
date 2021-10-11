import unittest
import os
import json
import shutil
from injectable import load_injection_container

from RegressionSeeker import RegressionSeeker

def getJson(path):
    with open(path) as f:
        return json.load(f)

class BasicTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        results_path="results/SpringBootSamples"
        if os.path.exists(results_path):
            shutil.rmtree(results_path)

        load_injection_container()
        project="SpringBootSamples"
        bug="1"
        rs = RegressionSeeker(project, bug)
        rs.searchRegression()
        rs.finish("FINISH ON TEST MODE")

    def test_regression_test_exist(self):
        testPath = "results/SpringBootSamples/Bug_1/DividerTest.java"
        self.assertTrue(
            os.path.isfile(testPath),
            "The regression test should be stored"
        )
    
    def test_fix_commit(self):
        result = getJson("results/SpringBootSamples/Bug_1/commits/0-add8221fb5314265ce7d7a8a4002078a498511a3/result.json")
        self.assertTrue(
            result['isTestExecutionSuccess'],
            "The test should pass on FIX commit"
        )

    def test_prev_commit(self):        
        result = getJson("results/SpringBootSamples/Bug_1/commits/1-e20b61b3d27954afabfc6a3675176adcdb47cfb6/result.json")
        self.assertTrue(
            result['isTestBuildSuccess'],
            "The test should compile on PREV commit"
        )
        self.assertFalse(
            result['isTestExecutionSuccess'],
            "The test should not pass on PREV commit"
        )

if __name__ == '__main__':
    unittest.main(verbosity=2)
