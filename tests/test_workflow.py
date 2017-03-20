from triage.workflow import TriageWorkflow
from triage.repository import Repository
from triage.exceptions import ConfigurationException
from triage.issue import Issue

import pytest


## find_issues
def test_unconfigured_workflow_raises():
    """TriageWorkflow needs a repository"""
    workflow = TriageWorkflow()
    with pytest.raises(ConfigurationException):
        workflow.find_issues()


def test_issues_are_issue_instances(workflow_with_issues):
    issues = workflow_with_issues.find_issues()

    assert len(issues) > 0

    for issue, actions in issues:
        assert isinstance(issue, Issue)


def test_issues_are_associated_with_actions(workflow_with_issues):
    issues = workflow_with_issues.find_issues()

    assert len(issues) > 0

    for issue, actions in issues:
        assert isinstance(actions, list)
        for action in actions:
            assert action in TriageWorkflow.ACTIONS


def test_find_issues_calls_repository_search(mock_repository_with_issues):
    """Triage uses a configured repository to retrieve issues"""
    workflow = TriageWorkflow(mock_repository_with_issues)
    workflow.find_issues()

    assert mock_repository_with_issues.read_issues.called
## find_issues


## process_issues
def test_update_issues_is_not_implemented(
    workflow_with_issues,
    issues_with_selected_actions
):
    with pytest.raises(NotImplementedError):
        workflow_with_issues.process_issues(issues_with_selected_actions)


def test_process_issues_applies_label(
    mock_repository_with_issues,
    issues_with_selected_actions
):
    workflow = TriageWorkflow(mock_repository_with_issues)

    workflow.process_issues(issues_with_selected_actions)

    assert mock_repository_with_issues.update_issue.called
    mock_repository_with_issues.update_issue.assert_called_once_with(
        123,
        ['bug'],
    )

## process issues


@pytest.fixture
def issues():
    return [
        {
            'id': 123,
            'title': 'Issue title',
            'description': 'A detailed description',
            'state': 'opened',
            'labels': [],
        }
    ]


@pytest.fixture
def repository_with_issues(issues):
    repository = Repository()
    repository.issues = issues
    return repository


@pytest.fixture
def workflow_with_issues(repository_with_issues):
    return TriageWorkflow(repository_with_issues)


@pytest.fixture
def issues_with_selected_actions():
    return [{
        'id': 123,
        'action': {
            'name': 'Label',
            'value': 'bug'
        }
    }]


@pytest.yield_fixture
def mock_repository_with_issues(mocker, issues):
    mock_repository = mocker.patch(
        'triage.repository.Repository',
        autospec=True,
    )
    mock_repository.read_issues.return_value = issues

    return mock_repository
