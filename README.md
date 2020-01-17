# Hammond
a Simple notice server with simple web panel

## 环境
 - python==3.7.2
 - celery==4.4.0
 - 更多详情见`requiremens.txt`

## 运行
`web`静态资源和`api`用`nginx`做了分离，直接使用`docker-compose`运行
1. 安装`docker-compose`,参见[docker-compose](https://docs.docker.com/compose/install/)
2. 打包启动服务
```
docker-compose build
docker-compose up -d
```

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

## TODO
 - 接入`dingtalk`