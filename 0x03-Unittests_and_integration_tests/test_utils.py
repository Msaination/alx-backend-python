#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from parameterized import parameterized
import utils


class TestAccessNestedMap(unittest.TestCase):
    """Tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected) -> None:
        """Test access_nested_map returns expected result for given path."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)


if __name__ == "__main__":
    unittest.main()
