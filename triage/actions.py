class Action(object):
    pass


class AddIssueLabelAction(Action):
    NAME = 'Label'


class CloseIssueAction(Action):
    NAME = 'Close'
