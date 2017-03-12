from triage import Workflow, Repository

import pytest


def test_unconfigured_workflow_raises():
    workflow = Workflow()
    with pytest.raises(Exception):
        workflow.find_issues()


def test_issues_are_associated_with_actions(mocker):
    repository = Repository()
    repository.issues = [
        {
            'title': 'Issue title',
            'description': 'A detailed description',
            'state': 'opened',
            'tags': [],
        }
    ]

    workflow = Workflow(repository)
    issues = workflow.find_issues()

    assert len(issues) > 0

    for issue, actions in issues:
        assert isinstance(actions, list)
        for action in actions:
            assert action in Workflow.ACTIONS
