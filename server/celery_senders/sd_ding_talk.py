import time
import hmac
import hashlib
import base64
from urllib import parse
import requests

from celery_senders.base_sender import BaseSender
from config import DINGTALK_SEC, DINGTALK_ACCESS_TOKEN


class DingTalkRobot(BaseSender):
    name = 'DingTalkRobot'

    def __init__(self, *args, **kwargs):
        self.secret = DINGTALK_SEC
        self.access_token = DINGTALK_ACCESS_TOKEN
        super(DingTalkRobot, self).__init__(*args, **kwargs)

    def calc_sign(self):
        # 把timestamp+"\n"+密钥当做签名字符串，使用HmacSHA256算法计算签名，然后进行Base64 encode
        # 最后再把签名参数再进行urlEncode，得到最终的签名（需要使用UTF-8字符集）
        timestamp = int(time.time() * 1000)
        secret = self.secret
        secret_enc = secret.encode('utf-8')
        # 把timestamp+"\n"+密钥当做签名字符串
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        # 使用HmacSHA256算法计算签名
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        # 进行Base64 encode把签名参数再进行urlEncode
        sign = parse.quote(base64.b64encode(hmac_code))
        return timestamp, sign

    def send_dingtalk_msg(self, title, content):
        """
        :param text: 消息标题，最长为256，必填。
        :param desp: 消息内容，最长64Kb，可空，支持MarkDown。
        :return:
        """
        timestamp, sign = self.calc_sign()
        url = 'https://oapi.dingtalk.com/robot/send?access_token={access_token}&timestamp={timestamp}&sign={sign}'. \
            format(
            access_token=self.access_token,
            timestamp=timestamp,
            sign=sign
        )
        playload_text = {
            "msgtype": "text",
            "text": {
                "content": content
            },
            "at": {
                "atMobiles": [],
                "isAtAll": False
            }
        }

        r = requests.post(url, json=playload_text, timeout=30).content.decode()
        self.logger.info(r)
        return r

    def send(self, title, content):
        self.send_dingtalk_msg(title, content)


'https://oapi.dingtalk.com/robot/send?access_token=bcf4d5ce0a554533220d163360b27052f9b2678f0086f152e570cb23a02b10c5'
if __name__ == '__main__':
    d = DingTalkRobot()
    # print(d.calc_sign())
    d.send('a', 'xxx')
