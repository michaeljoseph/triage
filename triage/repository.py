class Repository(object):
    issues = []

    def search(self):
        return self.issues

    def update_issue(self, issue_id, labels):
        raise NotImplemented
