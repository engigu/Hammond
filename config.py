import os
from core.utils import Utils

REDIS_HOST = 'redis:6379' if Utils.run_in_docker() else '127.0.0.1:6352'


class Config:

    PROJECT_NAME = 'Hammond'

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    BACKEND_REDIS_URI = f'redis://{REDIS_HOST}/2'
    API_SERVER_PORT = 9643  # flask api port

    TEST_SEND_MSG_INTER_TIME = 1*60

    # webauth 认证
    HTTP_AUTH = {
        'hammond': 'abc321'
    }


class RedisStoreKeyConfig(Config):

    # string
    SEND_MAIL_KEY = 'sina-send-mail-account'

    # hash
    RECV_MAIL_KEY = 'recv-mail-accounts'

    # hash server酱
    RECV_SERVERCHAN_KEY = 'recv-serverchan-accounts'

    # hash server酱
    ALLOWED_SEC_KEY = 'allowed-sec-keys'

    # string
    TEST_SEND_MSG_INTER_KEY = 'test-msg-next-time'
