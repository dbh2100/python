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

    def test_length_raises_overflowerror(self):
        """Test that len(Omniset) raises OverflowError"""
        omniset = Omniset()
        with self.assertRaises(OverflowError):
            len(omniset)

    def test_issubset(self):
        """Test subset behavior of Omniset"""

        omniset = Omniset()
        other_set = {1, 2, 3}

        self.assertFalse(omniset.issubset(other_set))
        self.assertTrue(omniset.issubset(omniset))

    def test_issuperset(self):
        """Test superset behavior of Omniset"""

        omniset = Omniset()
        other_set = {1, 2, 3}

        self.assertTrue(omniset.issuperset(other_set))
        self.assertTrue(omniset.issuperset(omniset))

    def test_union(self):
        """Test union of Omniset with another set"""

        omniset = Omniset()

        # Test with one set
        other_set = {1, 2, 3}
        union = omniset.union(other_set)
        self.assertIs(union, omniset)

        # Test with multiple sets
        other_set2 = frozenset({4, 5, 6})
        union2 = omniset.union(other_set, other_set2)
        self.assertIs(union2, omniset)

    def test_intersection(self):
        """Test intersection of Omniset with another set"""

        omniset = Omniset()

        # Test with no arguments
        self.assertEqual(omniset.intersection(), omniset)

        # Test with one set
        other_set = {1, 2, 3}
        intersection = omniset.intersection(other_set)
        self.assertEqual(intersection, other_set)

        # Test with multiple sets
        other_set2 = frozenset({2, 3, 4})
        intersection2 = omniset.intersection(other_set, other_set2)
        self.assertEqual(intersection2, {2, 3})


if __name__ == '__main__':
    unittest.main()
