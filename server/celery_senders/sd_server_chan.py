import time

import requests

from celery_senders.base_sender import BaseSender
from config import SERVER_CHAN_KEY


class SeverChan(BaseSender):
    name = 'ServerChan'

    def __init__(self, *args, **kwargs):
        super(SeverChan, self).__init__(*args, **kwargs)

    def send_ftqq_msg(self, text, desp):
        """
        :param text: 消息标题，最长为256，必填。
        :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
        :return:
        """
        url = 'http://sc.ftqq.com/{}.send'.format(SERVER_CHAN_KEY)
        content = desp + '\n\nDate:  {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        r = requests.post(url, data={'text': text, 'desp': content}).content.decode()
        self.logger.info(r)
        return r

    def send(self, title, content):
        self.send_ftqq_msg(title, content)

