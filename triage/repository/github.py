from .core import Repository

class GithubRepository(Repository):
    config_schema = {
        'github_token': 'string',
        'owner': 'string',
        'repo': 'string'
    }
