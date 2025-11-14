#!/usr/bin/env python3
"""
fixtures.py
Fixtures for integration tests of GithubOrgClient.
"""

# Organization payload fixture
org_payload = {
    "login": "test-org",
    "id": 123,
    "repos_url": "https://api.github.com/orgs/test-org/repos",
}

# Repositories payload fixture
repos_payload = [
    {"id": 1, "name": "repo1", "license": {"key": "apache-2.0"}},
    {"id": 2, "name": "repo2", "license": {"key": "mit"}},
    {"id": 3, "name": "repo3", "license": {"key": "apache-2.0"}},
]

# Expected list of all repo names
expected_repos = ["repo1", "repo2", "repo3"]

# Expected list of repos filtered by apache-2.0 license
apache2_repos = ["repo1", "repo3"]
