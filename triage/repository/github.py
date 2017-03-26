from .core import Repository

import logging
from uritemplate import URITemplate
import requests

log = logging.getLogger(__name__)
READ_ISSUES = URITemplate('https://api.github.com/repos{/owner}{/repo}/issues')
UPDATE_ISSUE = URITemplate('https://api.github.com/repos{/owner}{/repo}/issues{/number}')


class GithubRepository(Repository):
    """
{
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
      "avatar_url": "https://avatars2.githubusercontent.com/u/169933?v=3",
      "gravatar_id": "",
      "url": "https://api.github.com/users/michaeljoseph",
      "html_url": "https://github.com/michaeljoseph",
      "followers_url": "https://api.github.com/users/michaeljoseph/followers",
      "following_url": "https://api.github.com/users/michaeljoseph/following{/other_user}",
      "gists_url": "https://api.github.com/users/michaeljoseph/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/michaeljoseph/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/michaeljoseph/subscriptions",
      "organizations_url": "https://api.github.com/users/michaeljoseph/orgs",
      "repos_url": "https://api.github.com/users/michaeljoseph/repos",
      "events_url": "https://api.github.com/users/michaeljoseph/events{/privacy}",
      "received_events_url": "https://api.github.com/users/michaeljoseph/received_events",
      "type": "User",
      "site_admin": false
    },
    "labels": [
      {
        "id": 52048165,
        "url": "https://api.github.com/repos/michaeljoseph/changes/labels/enhancement",
        "name": "enhancement",
        "color": "84b6eb",
        "default": true
      },
      {
        "id": 54927548,
        "url": "https://api.github.com/repos/michaeljoseph/changes/labels/ready",
        "name": "ready",
        "color": "00c5fe",
        "default": false
      }
    ],
    "state": "open",
    "locked": false,
    "assignee": null,
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
        "id": 169933,
        "avatar_url": "https://avatars2.githubusercontent.com/u/169933?v=3",
        "gravatar_id": "",
        "url": "https://api.github.com/users/michaeljoseph",
        "html_url": "https://github.com/michaeljoseph",
        "followers_url": "https://api.github.com/users/michaeljoseph/followers",
        "following_url": "https://api.github.com/users/michaeljoseph/following{/other_user}",
        "gists_url": "https://api.github.com/users/michaeljoseph/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/michaeljoseph/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/michaeljoseph/subscriptions",
        "organizations_url": "https://api.github.com/users/michaeljoseph/orgs",
        "repos_url": "https://api.github.com/users/michaeljoseph/repos",
        "events_url": "https://api.github.com/users/michaeljoseph/events{/privacy}",
        "received_events_url": "https://api.github.com/users/michaeljoseph/received_events",
        "type": "User",
        "site_admin": false
      },
      "open_issues": 2,
      "closed_issues": 0,
      "state": "open",
      "created_at": "2014-10-14T07:14:02Z",
      "updated_at": "2014-12-11T11:50:38Z",
      "due_on": null,
      "closed_at": null
    },
    "comments": 0,
    "created_at": "2014-09-28T17:52:04Z",
    "updated_at": "2016-07-23T16:30:02Z",
    "closed_at": null,
    "body": "https://github.com/borntyping/python-colorlog\n"
},
    """

    config_schema = {
        'github_token': 'string',
        'owner': 'string',
        'repo': 'string'
    }

    @property
    def headers(self):
        return {
            'Authorization': 'token {}'.format(self.config['github_token'])
        }

    def read_issues(self, filters=None):
        return requests.get(
            READ_ISSUES.expand(self.config),
            filters or {},
            headers=self.headers,
        ).json()

    def handle_label_issue(self, action):
        issue_to_label = action.issue
        label_name = action.label
        log.debug('Adding label {} to issue {}'.format(
            label_name, issue_to_label.number
        ))

        config = self.config.copy()
        config['number'] = str(issue_to_label.number)

        return requests.patch(
            UPDATE_ISSUE.expand(config),
            json={'labels': [label_name]},
            headers=self.headers
        )
