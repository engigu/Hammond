import time

import requests

from celery_senders.base_sender import BaseSender
from core.db import RedisModel
from config import Config, RedisStoreKeyConfig

REDIS_MODEL = RedisModel(uri=Config.BACKEND_REDIS_URI)


class SeverChan(BaseSender):
    name = 'ServerChan'

    def __init__(self, *args, **kwargs):
        self.receivers = self.get_args_from_redis()
        super(SeverChan, self).__init__(*args, **kwargs)

    def get_args_from_redis(self):
        receivers = REDIS_MODEL.list_all_receivers(
            RedisStoreKeyConfig.RECV_SERVERCHAN_KEY
        )
        receivers = [k for k, v in receivers.items() if v.get('is_recv', None)]
        return receivers

    def send_ftqq_msg(self, server_key, text, desp):
        """
        :param text: 消息标题，最长为256，必填。
        :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
        :return:
        """
        url = 'http://sc.ftqq.com/{}.send'.format(server_key)
        content = desp + \
            '\n\nDate:  {}'.format(time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        r = requests.post(
            url, data={'text': text, 'desp': content}).content.decode()
        self.logger.info(r)
        return r

    def send(self, title, content):
        for key in self.receivers:
            self.send_ftqq_msg(key, title, content)
