import requests


class Cli:
    def __init__(self):
        # self.server_url = 'http://sooko.club:8888/notice'
        self.server_url = 'http://127.0.0.1:9643/notice'
        # self.server_url = 'http://192.168.170.132:8890/notice'

    def send(self, way, title, content):
        data = {'title': title, 'content': content, 'way': way, 'key': 'spider_c:Lnh9fZYSZ9LHTRYrz7ragN', }
        return requests.post(url=self.server_url, data=data).content.decode()

    def test(self):
        # data = {'title': 1, 'content': '[(1,2), (3,6)]', 'way': 'SinaEmail'}
        data = {'title': 1, 'content': '[(1,2), (3,6)]', 'way': 'ServerChan'}
        print(self.send(**data))


if __name__ == '__main__':
    c = Cli()
    c.test()
