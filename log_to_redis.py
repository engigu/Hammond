# 跟踪log文件并写入redis，返回给前端页面
from core.db import Redis
from subprocess import run

from sh import tail


class LogToRedis(Redis):
    def __init__(self, uri):
        super().__init__(uri=uri)

    def exec_shell(self, shell):
        # res = run(shell, shell=True)
        # print(res)
        for line in tail("-n", "30", "-f", shell, _iter=True):
            print(line)

    def run(self):
        pass


if __name__ == "__main__":
    from config import Config

    ltr = LogToRedis(Config.BACKEND_REDIS_URI)
    ltr.exec_shell('logs/celery.log')
    pass
