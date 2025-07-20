#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_payload = {"payload": True}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns the correct URL"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/testorg/repos"}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/testorg/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns the list of repo names"""
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/testorg/repos"
            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
            mock_repos_url.assert_called_once()


if __name__ == "__main__":
    unittest.main()
