import unittest
import calc_tests
testLoad = unittest.TestLoader()
suites = testLoad.loadTestsFromModule(calc_tests)
testResult = unittest.TestResult()
runner = unittest.TextTestRunner( verbosity = 1 )
testResult = runner.run(suites)
print ( "errors" )
print ( len (testResult.errors))
print ( "failures" )
print ( len (testResult.failures))
print ( "skipped" )
print ( len (testResult.skipped))
print ( "testsRun" )
print (testResult.testsRun)

"""
Ran 6 tests in 0.001s
OK
errors
0
failures
0
skipped
0
testsRun
6
"""