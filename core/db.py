import base64
import redis
import json
from datetime import timedelta
import shortuuid

from config import Config, RedisStoreKeyConfig
from core.utils import Utils
from core.defined import ConfigKey


class SameOriginSingleton(type):
    """
    同样的连接uri只有一个实例
    """
    _instances = {}

    @staticmethod
    def calc_params_identify(params):
        return base64.b64encode(str(params).encode())

    def __call__(cls, *args, **kwargs):
        params_ident = cls.calc_params_identify(args)
        if params_ident not in cls._instances:
            cls._instances[params_ident] = super(
                SameOriginSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[params_ident]


class Redis(metaclass=SameOriginSingleton):
    def __init__(self, uri):
        self.redis_client = self.init_redis(uri)

    def init_redis(self, uri):
        return redis.StrictRedis(
            connection_pool=redis.ConnectionPool.from_url(uri),
            decode_responses=True
        )


class RedisModel(Redis):
    # 获取负责发送的邮箱帐号密码
    def get_send_mail(self):
        account = self.redis_client.get(RedisStoreKeyConfig.SEND_MAIL_KEY)
        if not account:
            return {'account': '', 'password': ''}
        return json.loads(account.decode())

    def update_send_mail(self, account, password):
        return self.redis_client.set(
            RedisStoreKeyConfig.SEND_MAIL_KEY,
            json.dumps({'account': account, 'password': password}))

    def add_receiver(self, redis_key, account):
        if redis_key == ConfigKey.allowed_sec_keys:
            # 此时生成安全密钥，参数穿过只作为前缀
            # 完整密钥需要再次生成
            account = f'{account}:{shortuuid.uuid()}'

        record = self.redis_client.hget(
            redis_key,
            account
        )
        if record:
            return f'{account} has exists!'

        account_info = {
            'is_recv': 1,
            'modified': Utils.now(),
        }
        self.redis_client.hset(
            redis_key, account,
            json.dumps(account_info, ensure_ascii=False)
        )
        return 'ok!'

    def list_all_receivers(self, redis_key):
        result = self.redis_client.hgetall(redis_key)
        return {k.decode(): json.loads(v) for k, v in result.items()}

    def delete_receiver(self, redis_key, account):
        self.redis_client.hdel(
            redis_key, account
        )

    def update_receiver(self, redis_key, account, is_recv):

        account_info = {
            'is_recv': is_recv,
            'modified': Utils.now(),
        }
        self.redis_client.hset(
            redis_key, account,
            json.dumps(account_info, ensure_ascii=False)
        )

    def vaild_sec_key(self, sec_key):

        result = self.redis_client.hget(
            RedisStoreKeyConfig.ALLOWED_SEC_KEY, sec_key
        )

        if not result:
            return False

        is_recv = json.loads(result).get('is_recv', None)
        return bool(is_recv)

    def can_send_test_msg(self):
        rtime = self.redis_client.get(RedisStoreKeyConfig.TEST_SEND_MSG_INTER_KEY)
        if not rtime:
            self.redis_client.set(
                RedisStoreKeyConfig.TEST_SEND_MSG_INTER_KEY,
                (Utils.now(return_datetime=True) + timedelta(seconds=Config.TEST_SEND_MSG_INTER_TIME)).strftime('%Y-%m-%d %H:%M:%S')
                )
            return True
        
        rtime = rtime.decode()
        if Utils.now() > rtime:
            return True

        return rtime  # false
