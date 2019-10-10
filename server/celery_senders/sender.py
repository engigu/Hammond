# -*- coding: utf-8 -*-
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from celery import Celery
from celery.utils.log import get_task_logger

app = Celery('sender')  # 创建 Celery 实例
app.config_from_object('celery_senders.celery_config')  # 通过 Celery 实例加载配置模块

logger = get_task_logger(__name__)

# ALL_SENDERS = load_module('.', __file__, 'sd_')
# ALL_SENDERS = {v.name: v for k, v in ALL_SENDERS.items()}
from celery_senders.sd_sina_email import SinaSmtpSender
from celery_senders.sd_server_chan import SeverChan

ALL_SENDERS = {
    SinaSmtpSender.name: SinaSmtpSender,
    SeverChan.name: SeverChan
}


@app.task
def send_notice(way, title, content):
    sender = ALL_SENDERS.get(way, None)
    if not sender:
        raise Exception('way: {} error'.format(way))
    logger.info('way: %r, title: %r, content: %r' % (way, title, content))
    sender = sender()
    sender.send(title, content)
