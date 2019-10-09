import logging

import tornado.ioloop
import tornado.web
import tornado.log

from core.utils import load_module

tornado.log.enable_pretty_logging()

ALL_SENDERS = load_module('celery_senders', __file__, 'sd_')
ALL_SENDERS = {v.name: v for k, v in ALL_SENDERS.items()}
logging.info(f'load celery_senders: {str(ALL_SENDERS)}')


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


#
# def args(func):
#     def args_wrapper(self, *args, **kwargs):
#         print(args)
#         print(kwargs)
#         print(self)
#         for k, v in kwargs:
#             if k in self.json_args:
#                 kwargs[v] = self.json_args[k]
#         return func(self, *args, **kwargs)
#
#     return args_wrapper


class MainHandler(BaseRequestHandler):
    def get(self):
        self.write("Hello, world")

    # @args
    def post(self):
        way = self.get_body_argument('way')
        title = self.get_body_argument('title')
        content = self.get_body_argument('content')
        # print(self.request.body)
        if not (title and content):
            raise Exception('params error')

        if way not in ALL_SENDERS:
            raise Exception('send way error')
        try:
            s = ALL_SENDERS[way]()
            s.send(title, content)
            self.finish({'msg': 'ok!'})
        except Exception as e:
            logging.exception(e)
            self.finish({'msg': 'not ok!'})


def make_app():
    return tornado.web.Application([
        (r"/notice", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
