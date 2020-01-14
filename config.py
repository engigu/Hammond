import os
from core.utils import Utils


class Config:

    ROOT_PATH =  os.path.dirname(os.path.abspath(__file__))

    SQLITE_URI =  f'sqlite:///{ROOT_PATH}/sqlite.db'

    PROJECT_NAME = 'cookies_pool'

    COOKIES_KEY_FORMAT = '%(site)s:cookies:%(no)s'

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    # REDIS_URI = 'redis://192.168.244.128:6379/2'
    REDIS_URI = 'redis://127.0.0.1:6352/2' if not Utils.run_in_docker() else 'redis://redis:6379/2'

    SLEEP_LOOP_TIME = 5 * 60

    API_SERVER_PORT = 9632



# #
# #
# #
# #
# #
# #
# import os

# ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# SERVER_PORT = 8888

# #################################
# # 渠道key, 只有匹配了key，才会发送
# SEC_KEYS = [
#     'own:EHkmdeTvVgzEJADz32ENZC',  # 自己的一系列服务
#     'spider_c:TFvkD9enEkvkVUyMVJUYmN',  # 公司的爬虫业务
# ]
# #################################


# #
# # 各种账号的配置
# ###########  新浪邮箱  ############
# SINA_SMTP_USER = b'dG90YWxjaGVja0BzaW5hLmNvbQ=='
# SINA_SMTP_PASS = b"Z3ExOTk0MDUwNw=="
# SINA_SMTP_RECEIVERS = [b"c2F5aGV5YUBxcS5jb20="]

# ###########  Server酱  ############
# SERVER_CHAN_KEY = 'SCU30620T7f7c14060cb17921326cbe6eb83344f25b70f4f1e24ab'

# ###########  DINGDING  ############
# DINGTALK_SEC = 'SECe8abed6948d916717d4bb021a13704100a9037ae8172ba7078addffc3a1eb748'
# DINGTALK_ACCESS_TOKEN = 'bcf4d5ce0a554533220d163360b27052f9b2678f0086f152e570cb23a02b10c5'
