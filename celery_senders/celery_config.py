from config import REDIS_HOST


BROKER_URL = f'redis://{REDIS_HOST}/10'               # 指定 Broker
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}/11'  # 指定 Backend
CELERY_TIMEZONE = 'Asia/Shanghai'                     # 指定时区，默认是 UTC
# CELERY_TIMEZONE='UTC'
# CELERY_IMPORTS = (                                  # 指定导入的任务模块
#     'celery_app.task1',
#     'celery_app.task2'
# )
# WORKDIR  = r'F:\tmp\ameng\celery_senders'
CELERY_IMPORTS = ("celery_senders.sender",)
