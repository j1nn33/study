import unittest
import calc_tests

calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(calc_tests.CalcBasicTests))
calcTestSuite.addTest(unittest.makeSuite(calc_tests.CalcExTests))

runner = unittest.TextTestRunner( verbosity = 2 )
runner.run(calcTestSuite)

"""
test_add (calc_tests.CalcBasicTests) ... ok
test_div (calc_tests.CalcBasicTests) ... ok
test_mul (calc_tests.CalcBasicTests) ... ok
test_sub (calc_tests.CalcBasicTests) ... ok
test_pow (calc_tests.CalcExTests) ... ok
test_sqrt (calc_tests.CalcExTests) ... ok
-------------------------------------------------------------------
Ran 6 tests in 0.002s
OK
"""