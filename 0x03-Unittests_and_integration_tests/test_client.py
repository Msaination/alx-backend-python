#!/usr/bin/env python3
"""
test_client.py
Unit tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit test suite for GithubOrgClient."""

    @parameterized.expand([
        ("google", {"login": "google", "id": 1}),
        ("abc", {"login": "abc", "id": 2}),
    ])
    @patch("client.get_json")
    def test_org(self,
                 org_name: str,
                 expected_payload: Dict,
                 mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the correct value.

        Ensures get_json is called once with the expected URL
        and that no external HTTP calls are made.
        """
        # Arrange: mock get_json to return the expected payload
        mock_get_json.return_value = expected_payload

        # Act: create client and access org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called once with correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)


if __name__ == "__main__":
    unittest.main()
