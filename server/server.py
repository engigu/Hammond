import logging
from inspect import getfullargspec

import tornado.ioloop
import tornado.web
import tornado.log

from celery_senders.sender import send_notice
from config import SERVER_PORT
from core.utils import args, sec_check, load_module

tornado.log.enable_pretty_logging()

ALL_WAYS = load_module('celery_senders', __file__, 'sd_')
ALL_WAYS = {v.name: v for k, v in ALL_WAYS.items()}
print(ALL_WAYS)


class BaseRequestHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     try:
    #         # self.json_args = json.loads(self.request.body)
    #         post_data = self.request.body_arguments
    #         self.json_args = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
    #     except:
    #         self.json_args = 0
    #     # print(self.request.body_arguments)
    pass


class MainHandler(BaseRequestHandler):
    def get(self):
        self.write("Hello, world")

    @sec_check
    @args
    def post(self, way: str = '', title: str = '', content: str = ''):
        print(way, title, content)
        if not (title and content):
            self.finish({'msg': 'title or content params error!'})
            return
        if way not in ALL_WAYS:
            self.finish({'msg': 'way error!'})
            return

        send_notice.delay(way, title, content)
        self.finish({'msg': 'ok!'})


def make_app():
    return tornado.web.Application([
        (r"/notice", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(SERVER_PORT)
    logging.info("Start Success: 0.0.0.0:{}".format(SERVER_PORT))
    tornado.ioloop.IOLoop.current().start()
