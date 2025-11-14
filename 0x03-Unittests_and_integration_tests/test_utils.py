#!/usr/bin/env python3
"""
test_utils.py
Unit tests for utils.access_nested_map function.

This script uses unittest and parameterized to validate
the behavior of access_nested_map across multiple scenarios.

Usage:
    Run all tests:
        python3 test_utils.py
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test suite for the access_nested_map function.

    Validates correct value retrieval from nested mappings
    using various key path sequences.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self,
                               nested_map: Mapping[str, Any],
                               path: Sequence[str],
                               expected: Any) -> None:
        """
        Test that access_nested_map returns the expected value.

        Parameters
        ----------
        nested_map : Mapping[str, Any]
            The nested dictionary to traverse.
        path : Sequence[str]
            The sequence of keys to follow.
        expected : Any
            The expected value at the end of the path.
        """
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
