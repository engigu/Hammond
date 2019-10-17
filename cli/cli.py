import requests


class Cli:
    def __init__(self):
        # self.server_url = 'http://sooko.tk:8888/notice'
        self.server_url = 'http://127.0.0.1:8888/notice'

    def send(self, way, title, content):
        data = {'title': title, 'content': content, 'way': way, 'key': 'spider_c:TFvkD9enEkvkVUyMVJUYmN', }
        return requests.post(url=self.server_url, data=data).content.decode()

    def test(self):
        # data = {'title': 1, 'content': '[(1,2), (3,6)]', 'way': 'SinaEmail'}
        data = {'title': 1, 'content': '[(1,2), (3,6)]', 'way': 'ServerChan'}
        print(self.send(**data))


if __name__ == '__main__':
    c = Cli()
    c.test()
