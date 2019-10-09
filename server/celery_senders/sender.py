import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from celery_senders import app, load_module
from celery.utils.log import get_task_logger
# from core.utils import load_module



logger = get_task_logger(__name__)

ALL_SENDERS = load_module('.', __file__, 'sd_')
ALL_SENDERS = {v.name: v for k, v in ALL_SENDERS.items()}
print(99999, ALL_SENDERS)
logger.info(f'load celery_senders: {str(ALL_SENDERS)}')


@app.task
def send_notice(way, title, content):
    sender = ALL_SENDERS.get(way, None)
    if not sender:
        raise Exception('way: {} error'.format(way))
    sender = sender()
    sender.send(title, content)
