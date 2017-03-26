import pytest
from triage.issue import Issue


def test_issue_no_data():
    issue = Issue()
    assert issue.number is None


def test_issue_hydration(github_issue_json):
    issue = Issue(github_issue_json)
    assert issue.number == 83
    assert 'id' in issue.data
    assert issue.data['user'] == {
        'login': 'michaeljoseph',
        'id': 169933
    }


@pytest.fixture
def github_issue_json():
    return {
        "url": "https://api.github.com/repos/michaeljoseph/changes/issues/83",
        "repository_url": "https://api.github.com/repos/michaeljoseph/changes",
        "labels_url": "https://api.github.com/repos/michaeljoseph/changes/issues/83/labels{/name}",
        "comments_url": "https://api.github.com/repos/michaeljoseph/changes/issues/83/comments",
        "events_url": "https://api.github.com/repos/michaeljoseph/changes/issues/83/events",
        "html_url": "https://github.com/michaeljoseph/changes/issues/83",
        "id": 44236666,
        "number": 83,
        "title": "Colour",
        "user": {
            "login": "michaeljoseph",
            "id": 169933,
        },
        "labels": [
            {
                "id": 52048165,
                "url": "https://api.github.com/repos/michaeljoseph/changes/labels/enhancement",
                "name": "enhancement",
                "color": "84b6eb",
                "default": True
            },
            {
                "id": 54927548,
                "url": "https://api.github.com/repos/michaeljoseph/changes/labels/ready",
                "name": "ready",
                "color": "00c5fe",
                "default": False
            }
        ],
        "state": "open",
        "locked": False,
        "assignee": None,
        "assignees": [

        ],
        "milestone": {
            "url": "https://api.github.com/repos/michaeljoseph/changes/milestones/3",
            "html_url": "https://github.com/michaeljoseph/changes/milestone/3",
            "labels_url": "https://api.github.com/repos/michaeljoseph/changes/milestones/3/labels",
            "id": 825100,
            "number": 3,
            "title": "0.8.0 - UI and Prompts",
            "description": "",
            "creator": {
                "login": "michaeljoseph",
            },
        },
        "comments": 0,
        "created_at": "2014-09-28T17:52:04Z",
        "updated_at": "2016-07-23T16:30:02Z",
        "closed_at": None,
        "body": "https://github.com/borntyping/python-colorlog\n"
    }
