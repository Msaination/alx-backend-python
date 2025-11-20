#!/usr/bin/env python3
"""
test_utils.py
Unit tests for utils.access_nested_map, 
utils.get_json, and utils.memoize
functions.

This script uses unittest and parameterized to validate
the behavior of utility functions across multiple scenarios.

Usage:
    Run all tests:
        python3 test_utils.py
"""

import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any, Dict
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test suite for the access_nested_map function.
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
        """Test that access_nested_map returns the expected value."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map: Mapping[str, Any],
                                         path: Sequence[str],
                                         expected_key: str) -> None:
        """Test that access_nested_map raises KeyError for invalid paths."""
        with self.assertRaises(KeyError) as cm:
            utils.access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{expected_key}'")


class TestGetJson(unittest.TestCase):
    """
    Unit test suite for the get_json function.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self,
                      test_url: str,
                      test_payload: Dict[str, Any]) -> None:
        """Test that get_json returns the expected payload."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = utils.get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """
    Unit test suite for the memoize decorator.
    """

    def test_memoize(self) -> None:
        """Test that memoize caches the result and calls the method only once."""

        class TestClass:
            def a_method(self) -> int:
                return 42

            @utils.memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(
            TestClass,
            "a_method",
            return_value=42
        ) as mock_method:
            obj = TestClass()

            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()



if __name__ == "__main__":
    unittest.main()