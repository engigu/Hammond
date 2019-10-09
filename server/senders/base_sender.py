import base64


class BaseSender:
    name = 'BaseSender'

    # def __init__(self, *args, **kwargs):
    #     pass

    def _send(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass

    def decode_base64(self, raw):
        return base64.b64decode(raw).decode()
