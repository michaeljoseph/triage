from triage import Workflow


def test_workflow_finds_issues():
    workflow = Workflow()
    assert [] == workflow.find_issues()
