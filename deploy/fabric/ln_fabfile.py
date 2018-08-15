# -*- coding: utf-8 -*-
# 使用了绝对路径，替换为自己项目路径
from fabric import task, Connection, SerialGroup


@task
def deploy(c):
    c.run('cd /data/app/original/original')
    c.run('git stash')
    c.run('git checkout master')
    c.run('git pull origin master')
    c.run('source /data/vens/original/bin/activate')
    c.run('/data/vens/original/bin/pip install -r /data/app/original/requirements/base.txt')
    c.run('/data/vens/original/bin/python /data/app/original/original/manage.py migrate --settings=config.settings.production')
    c.run('sudo supervisorctl restart original')
    c.run('sudo supervisorctl status')
