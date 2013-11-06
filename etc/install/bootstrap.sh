#!/bin/bash

# Config
PROJECT_NAME=gopython3
USER=futurecolors

CODENAME=precise
PGSQL_VERSION=9.3
PROJECT_DIR=/home/vagrant/$PROJECT_NAME


# Update package list
apt-get update -y
apt-get install -y python-software-properties
add-apt-repository -y ppa:fkrull/deadsnakes  # python
add-apt-repository -y ppa:chris-lea/node.js  # node
apt-get update -y
# Python
apt-get install -y build-essential python3.3 python python-dev
# Dependencies for image processing
apt-get install -y imagemagick libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev
# Git (that's how we deploy)
apt-get install -y git
# Nginx
apt-get install nginx-all
# Nodejs
apt-get install -y nodejs

# our alterego
adduser --home /home/$USER --disabled-password futurecolors --gecos ""

# pip
su -l futurecolors
wget --quiet -O - https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python3.3
pip install virtualenvwrapper

# Postgresql PGSQL_VERSION
if ! command -v psql; then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $CODENAME-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | apt-key add -
    apt-get update -y
    apt-get install -y postgresql-$PGSQL_VERSION libpq-dev
    cp /vagrant/etc/install/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
    /etc/init.d/postgresql reload
fi

# Nginx
rm -f /etc/nginx/sites-enabled/default
cp /vagrant/etc/install/nginx.config /etc/nginx/sites-available/$PROJECT_NAME
invoke-rc.d nginx start

# Less
npm config set loglevel error
npm install -g less
