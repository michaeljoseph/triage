from .core import Repository

from uritemplate import URITemplate
import requests


READ_ISSUES = URITemplate('https://api.github.com/repos{/owner}{/repo}/issues')
UPDATE_ISSUE = URITemplate('https://api.github.com/repos{/owner}{/repo}/issues{/id}')


class GithubRepository(Repository):
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
            headers=self.headers
        )

    def update_issue(self, issue_id, label):
        config = dict(**self.config)
        config['id'] = issue_id
        return requests.patch(
            UPDATE_ISSUE.expand(config),
            headers=self.headers
        )
