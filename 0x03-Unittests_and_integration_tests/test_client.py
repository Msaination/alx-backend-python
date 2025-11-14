#!/usr/bin/env python3
"""
test_client.py
Unit tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from typing import Dict, List
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
        """Test that GithubOrgClient.org returns the expected payload."""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self) -> None:
        """Test that _public_repos_url returns the correct URL."""
        expected_url = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected_url}
        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test-org")
            result = client._public_repos_url
            self.assertEqual(result, expected_url)

    def test_public_repos(self) -> None:
        """
        Test that public_repos returns the expected list of repo names
        based on the mocked repos_payload.
        """
        repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
        ]
        expected_repos: List[str] = ["repo1", "repo2"]

        with patch.object(GithubOrgClient, "repos_payload",
                          new_callable=PropertyMock) as mock_repos:
            mock_repos.return_value = repos_payload
            client = GithubOrgClient("test-org")
            result = client.public_repos()
            self.assertEqual(result, expected_repos)


if __name__ == "__main__":
    unittest.main()
