FROM python:3.7-alpine

LABEL MAINTAINER="sayheya@163.com"

ADD requirements.txt /code/requirements.txt

ENV TZ=Asia/Shanghai
ENV RUN_IN_DOCKER=yes

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
	&& apk update \
    && apk add tzdata \
    && echo "${TZ}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && rm /var/cache/apk/* \
	&& pip install -r /code/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /code
WORKDIR /code/celery_senders

CMD celery -A sender worker --loglevel=info 
