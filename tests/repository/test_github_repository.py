import pytest

from triage.exceptions import ConfigurationException
from triage.issue import Issue
from triage.repository.github import GithubRepository
from triage.actions import LabelIssue


def test_github_repository_demands_configuration():
    with pytest.raises(ConfigurationException):
        GithubRepository()


def test_gh_repo_partial_configuration():
    with pytest.raises(ConfigurationException) as err:
        GithubRepository({'github_token': 'bar'})

    assert str(err.value) == 'Missing configuration key(s): owner,repo'


@pytest.fixture
def repository_config():
    return {
        'github_token': 'foo',
        'owner': 'michaeljoseph',
        'repo': 'changes'
    }


def test_configured_gh_repo(repository_config):
    GithubRepository(repository_config)


@pytest.fixture
def mock_github_requests(mocker):
    return mocker.patch(
        'triage.repository.github.requests',
        autospec=True,
    )


def test_read_issues_requests_github_api(repository_config, mock_github_requests):
    GithubRepository(repository_config).read_issues()

    mock_github_requests.get.assert_called_once_with(
        'https://api.github.com/repos/michaeljoseph/changes/issues',
        {},
        headers={'Authorization': 'token foo'}
    )


def test_read_issues_with_filter_params(repository_config, mock_github_requests):
    filters = {
        'state': 'open',
    }
    GithubRepository(repository_config).read_issues(filters)

    mock_github_requests.get.assert_called_once_with(
        'https://api.github.com/repos/michaeljoseph/changes/issues',
        filters,
        headers={'Authorization': 'token foo'}
    )


def test_handle_label_issue(repository_config, mock_github_requests):
    issue = LabelIssue(Issue({'number': '123'}), label='bug')

    GithubRepository(repository_config).handle_label_issue(issue)

    mock_github_requests.patch.assert_called_once_with(
        'https://api.github.com/repos/michaeljoseph/changes/issues/123',
        json={'labels': ['bug']},
        headers={'Authorization': 'token foo'}
    )
