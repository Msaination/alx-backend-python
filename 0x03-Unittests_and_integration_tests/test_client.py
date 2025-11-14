#!/usr/bin/env python3
"""
test_client.py
Unit tests for client.GithubOrgClient class.

This script validates that the org method correctly calls
get_json with the expected URL and returns the mocked payload.

Usage:
    Run all tests:
        python3 test_client.py
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from typing import Dict
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit test suite for GithubOrgClient.org method.
    """

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
        Test that GithubOrgClient.org returns the expected payload.

        Parameters
        ----------
        org_name : str
            GitHub organization name.
        expected_payload : Dict
            Mocked JSON response to return.
        mock_get_json : Mock
            Patched get_json function.
        """
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)
    
    def test_public_repos_url(self) -> None:
        """
        Test that _public_repos_url returns the correct URL
        based on the mocked org payload.
        """
        expected_url = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected_url}

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=property
        ) as mock_org:
            mock_org.return_value = payload

            client = GithubOrgClient("test-org")
            result = client._public_repos_url

            self.assertEqual(result, expected_url)
        
if __name__ == "__main__":
    unittest.main()
