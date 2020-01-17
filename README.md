# Hammond
a Simple notice server with simple web panel

![2020-01-17 20-49-33](https://user-images.githubusercontent.com/24751376/72613665-25ff6580-396b-11ea-99fc-da92d9d5fe9b.png)

## 环境
 - python==3.7.2
 - celery==4.4.0
 - 更多详情见`requiremens.txt`

## 运行
`web`静态资源和`api`用`nginx`做了分离，直接使用`docker-compose`运行
1. 安装`docker-compose`,参见[docker-compose](https://docs.docker.com/compose/install/)
2. 启动服务
```
docker-compose build
docker-compose up -d
```
3. 服务开启，访问`8890`端口

## 说明
 - 如果需要清空`redis`进行初始化,执行以下
 ```
 docker-compose exec notice-server python core/db.py init
 ```
 - `redis`数据库文件默认挂载在` /data/docker/hammond/`
 - `celery`服务里的启动是
 ```
celery -A sender worker --loglevel=info
 ```
 - `client`推送消息参考`cli/cli.py`
 - `http-auth`默认帐号密码`hammond` `abc321`

## TODO
 - 接入`dingtalk`
