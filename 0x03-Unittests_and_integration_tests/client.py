#!/usr/bin/env python3
"""
client.py
GitHub organization client for accessing public repository data.

Provides:
    - org: memoized organization metadata
    - public_repos: list of public repositories (optionally filtered by license)
    - has_license: static method to check license key

Usage:
    >>> client = GithubOrgClient("google")
    >>> client.public_repos()
    ['repo1', 'repo2', ...]
"""

from typing import List, Dict
from utils import get_json, access_nested_map, memoize


class GithubOrgClient:
    """
    A GitHub organization client.

    Fetches organization metadata and public repositories
    using the GitHub REST API.
    """

    ORG_URL = "https://api.github.com/orgs/{org}"

    def __init__(self, org_name: str) -> None:
        """
        Initialize the client with the organization name.

        Parameters
        ----------
        org_name : str
            GitHub organization name.
        """
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """
        Fetch and memoize organization metadata.

        Returns
        -------
        Dict
            JSON response containing organization details.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """
        Retrieve the public repositories URL from org metadata.

        Returns
        -------
        str
            URL to fetch public repositories.
        """
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """
        Fetch and memoize public repositories payload.

        Returns
        -------
        Dict
            JSON response containing repository data.
        """
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """
        List public repositories, optionally filtered by license.

        Parameters
        ----------
        license : str, optional
            License key to filter repositories.

        Returns
        -------
        List[str]
            List of repository names.
        """
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]
        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """
        Check if a repository has the specified license.

        Parameters
        ----------
        repo : Dict[str, Dict]
            Repository metadata.
        license_key : str
            License key to check.

        Returns
        -------
        bool
            True if license matches, False otherwise.
        """
        assert license_key is not None, "license_key cannot be None"
        try:
            return access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False


def main() -> None:
    """Run a demo fetch for a known organization."""
    client = GithubOrgClient("google")
    print("Public repos:", client.public_repos())


if __name__ == "__main__":
    main()
