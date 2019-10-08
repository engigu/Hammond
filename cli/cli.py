import requests


class Cli:
    def __init__(self, server_url):
        self.server_url = server_url
        pass

    def test(self):
        data = {'title': 1, 'content': 2}
        print(requests.post(url=server_url, data=data).content.decode())
        # print(requests.get(url=server_url, params=data).content.decode())
        pass


if __name__ == '__main__':
    server_url = 'http://127.0.0.1:8888/notice'
    c = Cli(server_url)
    c.test()
