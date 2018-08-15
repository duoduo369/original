original
===
新一代 django 项目开发脚手架。

当你经常面临开发各种中小型项目，且需要支持微信登录、微信小程序逻辑的时候，
用这个脚手架会节省很多时间。

features
---
* python-social-auth 提供的oauth支持, 特别对微信相逻辑定制，例如unioinid
* 微信小程序登录
* 本站 oauth, access_token 支持
* 简单的account逻辑
* restframework
* supervisor+gunicore+nginx，配置文件
* cdn 图片上传，目前支持 qiniu


TODO
---
* redis 支持


项目路径
---
* /data/vens  python vens
* /data/app  所有项目根路径
* /data/var/supervisor  supervisor 运行文件目录，socket、pid
* /data/var/log  日志
* /etc/nginx  nginx 相关配置目录
* /etc/supervisor  supervisor  相关配置目录


单次部署
---

将fabric文件路径改为自己的配置

    sudo pip install fabric
    cd /data/app/original
    ln -s /data/app/original/deploy/fabric/ln_fabfile.py fabfile.py
    fab deploy
