from gopython3.settings import Prod


def prod():
    return dict(
        DJANGO_CONFIGURATION='Prod',
        SERVER_NAME='dash.fcolors.ru',
        INSTANCE_NAME='dash',
        SUDO_USER='dash',
        NAME='dash',
        DB_NAME=Prod.DATABASES['default']['NAME'],
        DB_USER=Prod.DATABASES['default']['USER'],
        DB_PASSWORD=Prod.DATABASES['default']['PASSWORD'],
        DB_ROOT_PASSWORD=Prod.DATABASES['default']['PASSWORD'],
        VCS='git',
        GIT_BRANCH='master',
        PROJECT_NAME='gopython3',
        PROJECT_DIR='/home/dash/src/dash/gopython3/',
        SRC_DIR='/home/dash/src/dash/gopython3/',
        ENV_DIR='/home/lava/envs/dash/',
    )