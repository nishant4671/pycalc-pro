import unittest
from calculator import PyCalc

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = PyCalc()
    
    def test_basic_operations(self):
        self.assertAlmostEqual(self.calc.calculate("2+3"), 5)
        self.assertAlmostEqual(self.calc.calculate("5-3"), 2)
        self.assertAlmostEqual(self.calc.calculate("2*3"), 6)
        self.assertAlmostEqual(self.calc.calculate("6/3"), 2.0)
    
    def test_exponentiation(self):
        self.assertAlmostEqual(self.calc.calculate("2**3"), 8)
        self.assertAlmostEqual(self.calc.calculate("2^3"), 8)  # Using ^ operator
        self.assertAlmostEqual(self.calc.calculate("3**2"), 9)
    
    def test_functions(self):
        self.assertAlmostEqual(self.calc.calculate("sqrt(9)"), 3)
        self.assertAlmostEqual(self.calc.calculate("sin(0)"), 0)
    
    def test_unit_conversion(self):
        self.assertAlmostEqual(self.calc.convert_units(10, 'cm', 'inch'), 3.93701, places=3)
        self.assertAlmostEqual(self.calc.convert_units(1, 'kg', 'lb'), 2.20462, places=3)
    
    def test_error_handling(self):
        self.assertTrue("Error" in self.calc.calculate("2/0"))
        self.assertTrue("Error" in self.calc.calculate("unknown_func(1)"))

if __name__ == '__main__':
    unittest.main()