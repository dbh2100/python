"""Unittests for the Omniset data structure."""

import unittest
from data_structures.omniset import Omniset

class OmnisetTest(unittest.TestCase):
    """Test Omniset class"""

    def test_contains_all_other_elements(self):
        """Test that Omniset contains all elements other than itself"""
        omniset = Omniset()
        self.assertIn(42, omniset)
        self.assertIn("hello", omniset)
        self.assertIn((1, 2, 3), omniset)
        self.assertIn(None, omniset)
        self.assertIn(..., omniset)
        self.assertIn(3.14159, omniset)

    def test_does_not_contain_itself(self):
        """Test that Omniset does not contain itself"""
        omniset = Omniset()
        self.assertNotIn(omniset, omniset)

    def test_singleton_behavior(self):
        """Test that Omniset is a singleton"""
        omniset1 = Omniset()
        omniset2 = Omniset()
        self.assertIs(omniset1, omniset2)

    def test_no_arguments_allowed(self):
        """Test that Omniset constructor does not accept arguments"""
        with self.assertRaises(TypeError):
            Omniset(1)
        with self.assertRaises(TypeError):
            Omniset(a=1)
        with self.assertRaises(TypeError):
            Omniset(1, 2, 3)


if __name__ == '__main__':
    unittest.main()
