import logging

import tornado.ioloop
import tornado.web
import tornado.log

from celery_senders.sender import send_notice

tornado.log.enable_pretty_logging()

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
        if not (title and content):
            raise Exception('params error')

        send_notice.delay(way, title, content)
        self.finish({'msg': 'ok!'})



def make_app():
    return tornado.web.Application([
        (r"/notice", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
