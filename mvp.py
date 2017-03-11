class GithubIssuesRepository(object):
    issues = []

    def __init__(self, items):
        self.issues = items

    def update(self, item):
        new_items = []
        for old_item in self.issues:
            if item['id'] == old_item['id']:
                new_items.append(item)
            else:
                new_items.append(old_item)
        self.issues = new_items


class TriageWorkflow(object):
    """Workflow class configured with filtering."""
    repository = None
    actions = []

    def __init__(self, repository):
        self.repository = repository
        self.actions = [
            'Pass',
            'Label',
        ]

    @property
    def issues(self):
        # TODO: apply filters
        return self.repository.issues

    def process(self, responses):
        for item, label in responses:
            item['labels'].append(label)
            self.repository.update(
                item,
            )


class CLIPresenter(object):
    workflow = None
    responses = []

    def __init__(self, workflow):
        self.workflow = workflow

    def run(self):
        prompt = ','.join(self.workflow.actions) + ' '

        for issue in self.workflow.issues:
            print(issue)
            answer = input(prompt)
            self.responses.append(
                [issue, answer]
            )
        print('\n%s' % self.responses)
        self.workflow.process(self.responses)
        print('\nnew items:\n%s' % self.workflow.repository.issues)


def main():
    issues = [
        {
            'id': 1,
            'title': 'This is an issue',
            'labels': [],
        }
    ]

    # FIXME: advertise the configuration it requires
    repo = GithubIssuesRepository(issues)

    # FIXME: workflow should self-configure
    workflow = TriageWorkflow(repo)

    # this is the application
    ui = CLIPresenter(workflow)
    ui.run()


if __name__ == '__main__':
    main()