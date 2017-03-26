from triage.exceptions import UnsupportedActionException
from triage.repository import Repository, camel_to_snake_case
from triage.actions import LabelIssue
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
    action = LabelIssue(Issue(), 'bug')

    with pytest.raises(UnsupportedActionException):
        repository.handle_action(action)
