from .exceptions import ConfigurationException
from . import actions
from .issue import Issue


class TriageWorkflow(object):
    ACTIONS = [
        actions.LabelIssue,
        actions.CloseIssue,
        actions.LabelAndCloseIssue,
    ]
    FILTERS = {
        'state': 'open',
        'labels': [],
    }

    def __init__(self, repository=None):
        self.repository = repository

    def find_issues(self):
        if not self.repository:
            raise ConfigurationException()

        issues_and_actions = []

        issues = self.repository.read_issues(self.FILTERS)

        for issue in issues:
            issues_and_actions.append(
                (Issue.from_dict(issue), self.ACTIONS)
            )
        return issues_and_actions

    def process_issues(self, issue_actions):
        for issue_action in issue_actions:
            issue_id = issue_action['id']
            label = issue_action['action']['value']
            self.repository.update_issue(issue_id, [label])
