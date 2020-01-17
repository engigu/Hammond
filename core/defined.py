#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 16:27
# @Author  : SayHeya
# @File    : status.py
# @Contact : sayheya@qq.com
# @Desc    : All variable's status should be defined here!!!!

from config import RedisStoreKeyConfig


class Type(type):
    def __contains__(cls, item):
        return item in cls.keys or item in cls.values

    @property
    def keys(cls):
        return [k for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def values(cls):
        return [v for k, v in cls.__dict__.items() if not k.startswith('__')]

    @property
    def items(cls):
        return {k: v for k, v in cls.__dict__.items() if not k.startswith('__')}


class ConfigKey(metaclass=Type):
    mail = RedisStoreKeyConfig.RECV_MAIL_KEY
    serverchan = RedisStoreKeyConfig.RECV_SERVERCHAN_KEY
    allowed_sec_keys = RedisStoreKeyConfig.ALLOWED_SEC_KEY


if __name__ == '__main__':

    print(ConfigKey.keys)
    print(ConfigKey.values)
    print(ConfigKey.items)
