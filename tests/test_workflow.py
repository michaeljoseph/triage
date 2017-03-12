from triage.workflow import Workflow
from triage.repository import Repository
from triage.exceptions import ConfigurationException

import pytest


def test_unconfigured_workflow_raises():
    workflow = Workflow()
    with pytest.raises(ConfigurationException):
        workflow.find_issues()


@pytest.fixture
def repository_with_issues():
    repository = Repository()
    repository.issues = [
        {
            'title': 'Issue title',
            'description': 'A detailed description',
            'state': 'opened',
            'tags': [],
        }
    ]
    return repository


def test_issues_are_associated_with_actions(repository_with_issues):
    workflow = Workflow(repository_with_issues)
    issues = workflow.find_issues()

    assert len(issues) > 0

    for issue, actions in issues:
        assert isinstance(actions, list)
        for action in actions:
            assert action in Workflow.ACTIONS
