from triage import Workflow

import pytest


def test_workflow_finds_issues():
    workflow = Workflow()
    with pytest.raises(Exception):
        workflow.find_issues()
