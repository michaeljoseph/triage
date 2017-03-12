from triage import Workflow

import pytest


def test_unconfigured_workflow_raises():
    workflow = Workflow()
    with pytest.raises(Exception):
        workflow.find_issues()

