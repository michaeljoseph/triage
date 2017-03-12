from .exceptions import ConfigurationException


class Workflow(object):
    ACTIONS = [
        'Label',
        'Close',
    ]

    def __init__(self, repository=None):
        self.repository = repository

    def find_issues(self):
        if not self.repository:
            raise ConfigurationException()

        issues_and_actions = []

        issues = self.repository.search()
        for issue in issues:
            issues_and_actions.append(
                (issue, self.ACTIONS)
            )
        return issues_and_actions
