#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient  # Assuming client.py has this class


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns the correct value"""
        mock_get_json.return_value = {"mocked": "value"}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url property"""
        client = GithubOrgClient("any_org")

        with patch.object(GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/any_org/repos"
            }
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/any_org/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected repos list"""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos

        client = GithubOrgClient("any_org")
        with patch.object(GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "fake_url"

            repos = client.public_repos()
            expected_repo_names = [repo["name"] for repo in test_repos]

            self.assertEqual(repos, expected_repo_names)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("fake_url")


if __name__ == "__main__":
    unittest.main()
