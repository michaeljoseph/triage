class Issue(object):
    def __init__(self, id, title, description, state, labels):
        self.id = id
        self.title = title
        self.description = description
        self.state = state
        self.labels = labels

    @staticmethod
    def from_dict(issue):
        return Issue(
            issue['id'],
            issue['title'],
            issue['description'],
            issue['state'],
            issue['labels'],
        )
