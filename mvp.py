class GithubIssuesRepository(object):
    items = []

    def __init__(self, items):
        self.items = items

    def update(self, item):
        new_items = []
        for old_item in self.items:
            if item['id'] == old_item['id']:
                new_items.append(item)
            else:
                new_items.append(old_item)
        self.items = new_items


class TriageWorkflow(object):
    repository = None
    actions = []

    def __init__(self, repository):
        self.repository = repository
        self.actions = [
            'Pass',
            'Label',
        ]

    @property
    def items(self):
        return self.repository.items

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

        for item in self.workflow.items:
            print(item)
            answer = input(prompt)
            self.responses.append(
                [item, answer]
            )


def main():
    issues = [
        {
            'id': 1,
            'title': 'This is an issue',
            'labels': [],
        }
    ]

    repo = GithubIssuesRepository(issues)

    workflow = TriageWorkflow(repo)

    ui = CLIPresenter(workflow)

    ui.run()

    print('\n%s' % ui.responses)

    workflow.process(ui.responses)
    print('\nnew items:\n%s' % workflow.repository.items)

if __name__ == '__main__':
    main()