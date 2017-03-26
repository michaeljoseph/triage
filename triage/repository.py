from triage.exceptions import UnsupportedActionException


class Repository(object):
    issues = []

    def read_issues(self, filters=None):
        return self.issues

    def update_issue(self, issue_id, labels):
        raise NotImplementedError

    def handle_action(self, action):
        method_name = camel_to_snake_case(
            type(action).__name__,
            prefix='handle'
        )
        if not self.supports_action(method_name):
            raise UnsupportedActionException()

    def supports_action(self, method_name):
        return (
            hasattr(self, method_name) and
            callable(getattr(self, method_name))
        )


def camel_to_snake_case(camel_name, prefix=''):
    snake_name = []
    for letter in camel_name:
        snake_name.append(
            '_{}'.format(letter.lower()) if letter.isupper()
            else letter

        )

    snake_name = ''.join(snake_name)
    if not prefix:
        # trim leading underscore
        return snake_name[1:]

    return '{}{}'.format(prefix, snake_name)

