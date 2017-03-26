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
    }

    def __init__(self, repository=None):
        self.repository = repository

    def find_issues(self):
        """List issues according to filters.

        Associates issues with actions and return.
        """
        if not self.repository:
            raise ConfigurationException('Repository required')

        issues_and_actions = []

        issues = self.filter_no_labels(
            self.repository.read_issues(self.FILTERS)
        )

        for issue in issues:
            issues_and_actions.append(
                (Issue(issue), self.ACTIONS)
            )
        return issues_and_actions

    def process_issues(self, issue_actions):
        for issue_action in issue_actions:
            issue_id = issue_action['issue']['number']
            label = issue_action['action']['value']
            self.repository.update_issue(issue_id, [label])
    @staticmethod
    def filter_no_labels(issues):
        return [issue for issue in issues if issue['labels'] == []]
