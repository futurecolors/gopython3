from time import sleep
from django.core.management.base import BaseCommand
from api.exceptions import RateLimitExceeded

from api.wrappers.github import GithubSearchWrapper, GithubWrapper


moscow_django_packages = [
    'django',
    'pillow',
    'django-model-utils',
    'django-compressor',
    'django-picklefield',
    'embedly',
    'pytils',
    'django-admin-sso',
    'django-storages',
    'django-s3-folder-storage',
    'docutils',
    'south',
    'requests',
    'django-admin-tools',
    'django-debug-toolbar',
    'nose',
    'django-nose',
    'mock',
    'psycopg2',
    'dj-database-url',
    'gunicorn',
]


class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.github_search = GithubSearchWrapper()
        self.github = GithubWrapper()

    def handle(self, *args, **options):
        self.parse_most_popular()
        # self.parse_moscowdjango_packages()

    def parse_moscowdjango_packages(self):
        for name in moscow_django_packages:
            successfull = False
            while not successfull:
                successfull = True
                try:
                    repo, owner = self.github_search.get_most_popular_repo(name)
                except RateLimitExceeded:
                    print('Sleeping...')
                    sleep(20)
                    print('Woke up!')
                    successfull = False
                self.get_and_print_info(owner, repo)

    def parse_most_popular(self):
        page_size = 100
        max_pages_amount = 100
        github_search = GithubSearchWrapper()
        for page_num in range(max_pages_amount):
            repos_info = github_search.ask_about_popular_repos(extra_params={
                'per_page': page_size,
                'page': page_num,
                'sort': 'stars',
                'q': 'language:python',
            })
            for repo, owner in [(r['name'], r['owner']['login']) for r in repos_info['items']]:
                self.get_and_print_info(owner, repo)
                print('*' * 100)

    def get_and_print_info(self, owner, repo):
        print(
            owner,
            repo,
            self.github.get_py3_fork_info(owner, repo),
            [i['title'] for i in self.github.get_py3_issues_info(owner, repo)],
            [p['title'] for p in self.github.get_py3_pull_requests(owner, repo)],
            sep='\t'
        )
