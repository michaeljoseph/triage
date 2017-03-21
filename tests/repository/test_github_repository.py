import pytest

from triage.exceptions import ConfigurationException
from triage.repository.github import GithubRepository


def test_github_repository_demands_configuration():
    with pytest.raises(ConfigurationException):
        GithubRepository()


def test_gh_repo_partial_configuration():
    with pytest.raises(ConfigurationException) as err:
        GithubRepository({'github_token': 'bar'})

    assert str(err.value) == 'Missing configuration key(s): owner,repo'
