#!/usr/bin/env python3
"""
test_client.py
Unit tests and integration tests for client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from typing import Dict
from client import GithubOrgClient
import fixtures


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self,
                         repo: Dict[str, Dict],
                         license_key: str,
                         expected: bool) -> None:
        """Test that has_license returns the correct boolean result."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos."""

    @classmethod
    def setUpClass(cls) -> None:
        """Start patcher for requests.get with fixture side effects."""
        cls.get_patcher = patch("utils.requests.get")

        def side_effect(url: str):
            mock_response = unittest.mock.Mock()
            if url == GithubOrgClient.ORG_URL.format(org="test-org"):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Stop patcher for requests.get."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns expected repo names."""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test that public_repos filters repos by license key."""
        client = GithubOrgClient("test-org")
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
