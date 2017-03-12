

class Workflow(object):
    def __init__(self, repository=None):
        self.repository = repository

    def find_issues(self):
        if not self.repository:
            raise Exception()
        return []
