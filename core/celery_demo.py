#tasks.py


from celery import Celery

app = Celery('tasks',  backend='redis://192.168.244.128:6379/0', broker='redis://192.168.244.128:6379/1') #配置好celery的backend和broker


@app.task  #普通函数装饰为 celery task
def add(x, y):
    import time

    time.sleep(10)
    return x + y

