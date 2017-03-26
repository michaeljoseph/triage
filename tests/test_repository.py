from triage.exceptions import UnsupportedActionException
from triage.repository import Repository, camel_to_snake_case
from triage.actions import LabelIssue, CloseIssue
from triage.issue import Issue

import pytest


def test_camel_snake_with_prefix():
    assert (
        camel_to_snake_case('LabelIssue', prefix='handle') ==
        'handle_label_issue'
    )


def test_camel_snake_no_prefix():
    assert (
        camel_to_snake_case('LabelAndCloseIssue') ==
        'label_and_close_issue'
    )


def test_unsupported_action_throws():
    repository = Repository()
    action = CloseIssue(Issue(), comment='This is no longer relevant.')

    with pytest.raises(UnsupportedActionException):
        repository.handle_action(action)


def test_label_action_handler_gets_called():
    repository = Repository()
    action = LabelIssue(Issue({'number': '987'}), 'bug')

    assert repository.handle_action(action) == 'Adding label bug to issue 987'
