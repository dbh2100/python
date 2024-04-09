from aleph_number import AlephNumber, INFINITY
import unittest

class TestAlephNumber(unittest.TestCase):
    
    def test_addition(self):
        
        #Addition between aleph number and int
        self.assertEqual(AlephNumber(4) + 3, AlephNumber(4))
        self.assertEqual(-9 + AlephNumber(4), AlephNumber(4))
        
        #Addition between aleph number and float
        self.assertEqual(AlephNumber(4) + -7.2, AlephNumber(4))
        self.assertEqual(3.5 + AlephNumber(4), AlephNumber(4))
        
        #Addition between two aleph numbers
        self.assertEqual(AlephNumber(4) + AlephNumber(1), AlephNumber(4))
        self.assertEqual(AlephNumber(4) + AlephNumber(6), AlephNumber(6))
        
        #Addition between aleph number and string, None, etc. not implemented
        for x in ('a', None, [3], (9,), INFINITY):
            with self.assertRaises(TypeError):
                AlephNumber(4) + x
            with self.assertRaises(TypeError):
                x + AlephNumber(4)
                
    def test_subtraction(self):
        
        #Subtraction between aleph number and int
        self.assertEqual(AlephNumber(4) - 3, AlephNumber(4))
        
        #Subtraction between aleph number and float
        self.assertEqual(AlephNumber(4) - -7.2, AlephNumber(4))
        
        #Subtraction between aleph number and string, None, other aleph number, etc. not implemented
        for x in ('a', None, [3], (9,), AlephNumber(1), AlephNumber(7)):
            with self.assertRaises(TypeError):
                AlephNumber(4) - x
            with self.assertRaises(TypeError):
                x - AlephNumber(4)
                
    def test_multiplication(self):
        
        #Multiplication between aleph number and int
        self.assertEqual(AlephNumber(4) * 3, AlephNumber(4))
        self.assertEqual(-9 * AlephNumber(4), AlephNumber(4))
        
        #Multiplication between aleph number and float
        self.assertEqual(AlephNumber(4) * -7.2, AlephNumber(4))
        self.assertEqual(3.5 * AlephNumber(4), AlephNumber(4))
        
        #Multiplication between two aleph numbers
        self.assertEqual(AlephNumber(4) * AlephNumber(1), AlephNumber(4))
        self.assertEqual(AlephNumber(4) * AlephNumber(6), AlephNumber(6))
        
        #Multiplication between aleph number and string, None, etc. not implemented
        for x in ('a', None, [3], (9,), INFINITY):
            with self.assertRaises((TypeError, OverflowError)):
                AlephNumber(4) * x
            with self.assertRaises((TypeError, OverflowError)):
                x * AlephNumber(4)
                
    def test_division(self):
    
        #Division between aleph number and int
        self.assertEqual(AlephNumber(4) / 3, AlephNumber(4))
        self.assertEqual(-9 / AlephNumber(4), 0)
        self.assertEqual(AlephNumber(4) // 3, AlephNumber(4))
        self.assertEqual(-9 // AlephNumber(4), 0)
        
        #Division between aleph number and float
        self.assertEqual(AlephNumber(4) / -7.2, AlephNumber(4))
        self.assertEqual(3.5 / AlephNumber(4), 0)
        self.assertEqual(AlephNumber(4) // -7.2, AlephNumber(4))
        self.assertEqual(3.5 // AlephNumber(4), 0)
        
        #Division between two aleph numbers
        self.assertEqual(AlephNumber(4) / AlephNumber(1), AlephNumber(4))
        self.assertEqual(AlephNumber(4) / AlephNumber(4), 1)
        self.assertEqual(AlephNumber(4) / AlephNumber(6), 0)
        self.assertEqual(AlephNumber(4) // AlephNumber(1), AlephNumber(4))
        self.assertEqual(AlephNumber(4) // AlephNumber(4), 1)
        self.assertEqual(AlephNumber(4) // AlephNumber(6), 0)
                
    def test_power(self):
        self.assertEqual(2 ** AlephNumber(4), AlephNumber(5))
        
    def test_comparison(self):
    
        #Aleph number should always be greater than finite int
        self.assertNotEqual(AlephNumber(4), 5000)
        self.assertLess(5000, AlephNumber(4))
        self.assertGreater(AlephNumber(4), 5000)
        self.assertLessEqual(5000, AlephNumber(4))
        self.assertGreaterEqual(AlephNumber(4), 5000)
        
        #Aleph number should always be greater than finite float
        self.assertNotEqual(AlephNumber(4), 5000.2)
        self.assertLess(5000.2, AlephNumber(4))
        self.assertGreater(AlephNumber(4), 5000.2)
        self.assertLessEqual(5000.2, AlephNumber(4))
        self.assertGreaterEqual(AlephNumber(4), 5000.2)
        
        #Comparison between aleph number and float infinity
        self.assertNotEqual(AlephNumber(4), INFINITY)
        with self.assertRaises(TypeError):
            AlephNumber(4) < INFINITY
        with self.assertRaises(TypeError):
            AlephNumber(4) <= INFINITY
        with self.assertRaises(TypeError):
            AlephNumber(4) > INFINITY
        with self.assertRaises(TypeError):
            AlephNumber(4) >= INFINITY
        
        #Comparison between aleph numbers
        self.assertEqual(AlephNumber(4), AlephNumber(4))
        self.assertNotEqual(AlephNumber(4), AlephNumber(6))
        self.assertTrue(AlephNumber(2) < AlephNumber(4) < AlephNumber(9))
        self.assertTrue(AlephNumber(9) > AlephNumber(4) > AlephNumber(2))
        self.assertTrue(AlephNumber(2) <= AlephNumber(4) <= AlephNumber(4) <= AlephNumber(9))
        self.assertTrue(AlephNumber(9) >= AlephNumber(4) >= AlephNumber(4) >= AlephNumber(2))
        
    def test_conversion(self):
        with self.assertRaises(OverflowError):
            int(AlephNumber(4))
        self.assertEqual(float(AlephNumber(4)), INFINITY)
        
if __name__ == '__main__':
    unittest.main()
