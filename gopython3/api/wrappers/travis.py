from api.abstract_wrappers import AbstractJsonApiWrapper


class TravisCI(AbstractJsonApiWrapper):
    base_url = 'https://api.travis-ci.org/'

    def repo_build_info(self, owner, repo):
        self.hammock = self.hammock.repos(owner, repo)
        return 'GET', {}

    def get_build_status(self, owner, repo):
        data = self.ask_about_repo_build_info(owner=owner, repo=repo)
        if data:
            return {
                'full_name': data['slug'],
                'last_build_status': 'passed' if data['last_build_status'] == 0 else 'failed',
                'last_build_finished_at': data['last_build_finished_at'],
            }
        else:
            return {'error': 'Not TravisCI info.'}