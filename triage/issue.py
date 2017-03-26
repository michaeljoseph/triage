ISSUE_FIELDS = ['number', 'title', 'body', 'state', 'labels']


class Issue(object):
    def __init__(self, data=None):
        data = data or {}
        for key in ISSUE_FIELDS:
            setattr(self, key, data.get(key))

        self.data = data
