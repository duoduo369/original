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
* cdn 图片上传，目前支持 qiniu、腾讯云
* 微信公众号jssdk签名
* sms, 支持云片、腾讯云
* 图形验证码
* redis 支持
* 二维码
* cms 用户权限

目录讲解
---
deploy, 部署有关文件

original, 主代码目录
  * config, 配置有关文件
  * common, 异常，常量，工具方法等
  * account, 账户
  * misc, 无法分类
  * quickdev, 开发时可以随手涂鸦的目录
  * templates, html 模板目录
  * static，静态文件目录


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

启用某些功能
---

#### 图片上传

    FILE_UPLOAD_BACKEND = 'qiniu'
    根据七牛配置将下面配置补全  
    FILE_UPLOAD_KEY = ''
    FILE_UPLOAD_SECRET = ''
    FILE_UPLOAD_BUCKET = ''
    FILE_CALLBACK_POLICY = {}

#### redis

    ENABLE_REDIS = False
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0

#### 短信验证码

SMS_BACKEND 支持 qcloud(腾讯), yunpian(云片),
注意个人开发者短信服务商有很多限制，例如模板中的变量所有文字相加不得超过10个字(云片),腾讯(12个字)

    SMS_BACKEND = ''
    SMS_QCLOUD_KEY = ''
    SMS_QCLOUD_SECRET = ''
    SMS_QCLOUD_DEFAULT_TEMPLATE_ID = ''

    SMS_YUNPIAN_KEY = ''
    SMS_YUNPIAN_SECRET = ''
    SMS_YUNPIAN_DEFAULT_TEMPLATE_ID = ''
