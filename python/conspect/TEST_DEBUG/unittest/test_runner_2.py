import unittest
import calc_tests


testCases = []
testCases.append(calc_tests.CalcBasicTests)
testCases.append(calc_tests.CalcExTests)
testLoad = unittest.TestLoader()
suites = []
for tc in testCases:
    suites.append(testLoad.loadTestsFromTestCase(tc))

res_suite = unittest.TestSuite(suites )

runner = unittest.TextTestRunner( verbosity = 2 )
runner.run(res_suite)