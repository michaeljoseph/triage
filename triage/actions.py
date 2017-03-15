class Action(object):
    name = None


class IssueAction(Action):
    pass


class LabelIssue(IssueAction):
    name = 'Label'


class CloseIssue(IssueAction):
    name = 'Close'


class LabelAndCloseIssue(LabelIssue, CloseIssue):
    name = 'Label and close'
