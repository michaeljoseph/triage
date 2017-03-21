class Repository(object):
    issues = []

    def read_issues(self, filters=None):
        return self.issues

    def update_issue(self, issue_id, labels):
        raise NotImplementedError
