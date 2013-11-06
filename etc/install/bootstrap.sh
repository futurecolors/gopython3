#!/bin/bash

# Config
PROJECT_NAME=gopython3

CODENAME=precise
PGSQL_VERSION=9.3
PROJECT_DIR=/home/vagrant/$PROJECT_NAME


# Update package list
apt-get update -y
# Python dev packages
apt-get install -y build-essential python python-dev
# Dependencies for image processing
apt-get install -y imagemagick libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev
# Git (that's how we deploy)
apt-get install -y git


# Postgresql PGSQL_VERSION
if ! command -v psql; then
    echo "deb http://apt.postgresql.org/pub/repos/apt/ $CODENAME-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
    wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
    apt-get update -y
    apt-get install -y postgresql-$PGSQL_VERSION libpq-dev
    cp $PROJECT_DIR/etc/install/pg_hba.conf /etc/postgresql/$PGSQL_VERSION/main/
    /etc/init.d/postgresql reload
fi


# Node.js
# http://stackoverflow.com/questions/16302436/install-nodejs-on-ubuntu-12-10
if ! command -v npm; then
    apt-get install -y python-software-properties g++ make
    add-apt-repository ppa:chris-lea/node.js
    apt-get update -y
    apt-get install -y nodejs
fi
# Less
npm config set loglevel error
npm install -g less
