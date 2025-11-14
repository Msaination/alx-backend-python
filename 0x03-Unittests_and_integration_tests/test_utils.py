#!/usr/bin/env python3
"""
test_utils.py
Unit tests for utils.access_nested_map and utils.get_json functions.

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

    Ensures JSON is correctly fetched and parsed
    without making real HTTP requests.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any]) -> None:
        """
        Test that get_json returns the expected payload.

        Parameters
        ----------
        test_url : str
            The URL to fetch JSON from.
        test_payload : Dict[str, Any]
            The mocked JSON payload to return.
        """
        with patch("utils.requests.get") as mock_get:
            # Create a mock response object
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function under test
            result = utils.get_json(test_url)

            # Ensure requests.get was called exactly once with test_url
            mock_get.assert_called_once_with(test_url)

            # Ensure the result matches the mocked payload
            self.assertEqual(result, test_payload)


if __name__ == "__main__":
    unittest.main()
