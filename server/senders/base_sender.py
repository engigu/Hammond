import base64
from core.logger import get_logger
import logging


class BaseSender:
    name = 'BaseSender'

    def __init__(self, *args, **kwargs):
        self.logger = logging.LoggerAdapter(get_logger(), extra={'way': self.name})
        pass

    def _send(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def decode_base64(self, raw):
        return base64.b64decode(raw).decode()
