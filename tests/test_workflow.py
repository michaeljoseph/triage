from triage.workflow import Workflow
from triage.repository import Repository
from triage.exceptions import ConfigurationException

import pytest


def test_unconfigured_workflow_raises():
    workflow = Workflow()
    with pytest.raises(ConfigurationException):
        workflow.find_issues()


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
    return Workflow(repository_with_issues)


def test_issues_are_associated_with_actions(repository_with_issues):
    workflow = Workflow(repository_with_issues)
    issues = workflow.find_issues()

    assert len(issues) > 0

    for issue, actions in issues:
        assert isinstance(actions, list)
        for action in actions:
            assert action in Workflow.ACTIONS


@pytest.yield_fixture
def mock_repository_with_issues(mocker, issues):
    mock_repository = mocker.patch(
        'triage.repository.Repository',
        autospec=True,
    )
    mock_repository.search.return_value = issues

    return mock_repository


def test_find_issues_calls_repository_search(mock_repository_with_issues):
    workflow = Workflow(mock_repository_with_issues)
    workflow.find_issues()

    assert mock_repository_with_issues.search.called


def test_process_issues_applies_label(mock_repository_with_issues):
    workflow = Workflow(mock_repository_with_issues)
    issues_with_selected_actions = [{
        'id': 123,
        'action': {
            'name': 'Label',
            'value': 'bug'
        }
    }]
    workflow.process_issues(issues_with_selected_actions)

    assert mock_repository_with_issues.update_issue.called
    mock_repository_with_issues.update_issue.assert_called_once_with(
        123,
        ['bug'],
    )
