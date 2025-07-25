#!/usr/bin/env python3
"""Unit tests & Integration tests for client.py"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized,parameterized_class
from client import GithubOrgClient
from fixtures import org_payload
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """Unit test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google", {"payload": True}),
        ("abc", {"payload": False}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected, mock_get_json):
        """Test org returns correct value"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test _public_repos_url returns expected result"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
            client = GithubOrgClient("test")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos method"""
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/test/repos"
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test/repos"
            )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected
        )


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Set up for integration test with fixtures"""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        cls.mock_get.side_effect = [
            unittest.mock.Mock(json=lambda: cls.org_payload),
            unittest.mock.Mock(json=lambda: cls.repos_payload),
        ]

    @classmethod
    def tearDownClass(cls):
        """Tear down patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected results"""
        client = GithubOrgClient("test_org")
        self.assertEqual(client.public_repos(), self.expected_repos)

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        # Setup mock responses for calls to get_json
        mock_get_json.side_effect = [
            {"repos_url": "https://api.github.com/orgs/testorg/repos"},  # org response
            [  # repos response
                {"name": "repo1", "license": {"key": "apache-2.0"}, "private": False},
                {"name": "repo2", "license": {"key": "mit"}, "private": False},
            ]
        ]

        client = GithubOrgClient("testorg")
        filtered_repos = client.public_repos(license="apache-2.0")

        self.assertEqual(filtered_repos, ["repo1"])
