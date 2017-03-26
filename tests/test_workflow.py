from triage.workflow import TriageWorkflow
from triage.repository.core import Repository
from triage.exceptions import ConfigurationException
from triage.issue import Issue

import pytest


def test_unconfigured_workflow_raises():
    """TriageWorkflow needs a repository"""
    workflow = TriageWorkflow()
    with pytest.raises(ConfigurationException):
        workflow.find_issues()


def test_issues_are_issue_instances(workflow_with_issues):
    issues = workflow_with_issues.find_issues()

    assert len(issues) == 1

    for issue, actions in issues:
        assert isinstance(issue, Issue)


def test_find_issues_filters_out_labelled_issues(issues_with_labels):
    repository = Repository()
    repository.issues = issues_with_labels

    issues = TriageWorkflow(repository).find_issues()

    assert len(issues) == 1


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


@pytest.fixture
def issues():
    return [
        {
            'number': 123,
            'description': 'A detailed description',
            'title': 'An issue with no labels',
            'body': 'A detailed description',
            'state': 'opened',
            'labels': [],
        }
    ]

@pytest.fixture
def issues_with_labels(issues):
    return issues + [{
        'number': 456,
        'title': 'An issue with labels',
        'body': 'A detailed description',
        'state': 'opened',
        'labels': [{
           'id': 789,
           'name': 'bug'
        }],
    }]


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
        'issue': {
            'number': 123,
        },
        'action': {
            'name': 'Label',
            'value': 'bug'
        }
    }]


@pytest.yield_fixture
def mock_repository_with_issues(mocker, issues):
    mock_repository = mocker.patch(
        'triage.repository.core.Repository',
        autospec=True,
    )
    mock_repository.read_issues.return_value = issues

    return mock_repository
