from api.abstract_wrappers import AbstractJsonApiWrapper


TRAVIS_CI_STATUS_MAP = {
    0: 'passed',
    1: 'failed'
}


class TravisCI(AbstractJsonApiWrapper):
    base_url = 'https://api.travis-ci.org/'

    def repo_build_info(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo)
        return 'GET', {}

    def get_build_status(self, owner, repo):
        data = self.ask_about_repo_build_info(owner=owner, repo=repo)
        if data:
            return {
                'url': 'https://travis-ci.org/%s' % data['slug'],
                'last_build_status': TRAVIS_CI_STATUS_MAP.get(data['last_build_status'], 'failed'),
                'last_build_finished_at': data['last_build_finished_at'],
            }
        else:
            return {'error': 'Not TravisCI info.'}
