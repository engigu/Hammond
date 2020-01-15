import base64
import redis
import json

from config import Config, RedisStoreKeyConfig
from core.utils import Utils


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


class CookiesPoolRedis(Redis):
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

    def add_mail_receiver(self, account):
        # 添加一个邮件接受者
        record = self.redis_client.hget(
            RedisStoreKeyConfig.RECV_MAIL_KEY,
            account
        )
        if record:
            return f'{account} has exists!'

        account_info = {
            'is_recv': 1,
            'modified': Utils.now(),
        }
        self.redis_client.hset(
            RedisStoreKeyConfig.RECV_MAIL_KEY, account,
            json.dumps(account_info, ensure_ascii=False)
        )
        return 'ok!'

    def list_all_mail_receivers(self):
        # 查询所有的邮件接受人
        result = self.redis_client.hgetall(RedisStoreKeyConfig.RECV_MAIL_KEY)
        return {k.decode(): json.loads(v) for k, v in result.items()}

    def delete_mail_receiver(self, account):
        self.redis_client.hdel(
            RedisStoreKeyConfig.RECV_MAIL_KEY, account
        )

    def update_mail_receiver(self, account, is_recv):
        account_info = {
            'is_recv': is_recv,
            'modified': Utils.now(),
        }
        self.redis_client.hset(
            RedisStoreKeyConfig.RECV_MAIL_KEY, account,
            json.dumps(account_info, ensure_ascii=False)
        )
