import unittest
import calc_tests


calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(calc_tests.CalcTest))
calcTestSuite.addTest(unittest.makeSuite(calc_tests.CalcExTests))
print ( "count of tests: " + str (calcTestSuite.countTestCases()) + " \n " )

runner = unittest.TextTestRunner( verbosity = 2 )
runner.run(calcTestSuite)