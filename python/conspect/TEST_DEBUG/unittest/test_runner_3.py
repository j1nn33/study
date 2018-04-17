import unittest
import calc_tests


testLoad = unittest.TestLoader()
suites = testLoad.loadTestsFromModule(calc_tests)
runner = unittest.TextTestRunner( verbosity = 2 )
runner.run(suites)