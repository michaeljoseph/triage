class Action(object):
    name = None


class IssueAction(Action):
    def __init__(self, issue=None):
        self.issue = issue


class LabelIssue(IssueAction):
    name = 'Label'

    def __init__(self, issue, label):
        super().__init__(issue)
        self.label = label


class CloseIssue(IssueAction):
    name = 'Close'

    def __init__(self, issue, comment=None):
        super().__init__(issue)
        self.comment = comment


class LabelAndCloseIssue(LabelIssue, CloseIssue):
    name = 'Label And Close'
