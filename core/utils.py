import importlib
import inspect
import os
from inspect import getfullargspec

from celery_senders.base_sender import BaseSender as Base
from config import SEC_KEYS


def load_module(module_path, file_path, prefix):
    """
    module_path: 模块路径    foo.boo
    file_path: 导入文件的绝对路径作为基准 C:/user/a.py
    :return: 动态加载spider文件夹下的以sp_开头的模块
    """

    def get_site_name(file_name):
        """rtc_hr58.py"""
        if isinstance(file_name.split('.')[0].split('_'), str):
            return file_name.split('.')[0].split('_')[-1]
        elif isinstance(file_name.split('.')[0].split('_'), list):
            return '_'.join(file_name.split('.')[0].split('_')[1:])

    def valid(obj):
        if inspect.isclass(obj):
            if Base in obj.__bases__:
                return obj
        return False

    base_path = os.path.dirname(file_path)
    base_path = base_path.replace('\\', '/')  # windows可能一个路径中两种斜杠，统一
    # print(base_path)
    if module_path == '.':
        module_file_path = base_path
    else:
        module_file_path = os.path.join(base_path, os.sep.join(module_path.split('.')))
    # print(module_file_path)
    files = [i for i in os.listdir(module_file_path) if i.startswith(prefix)]
    # print(files)
    if module_path == '.':
        modules = {
            get_site_name(i): importlib.import_module('{}'.format(i.split('.py')[0]))
            for i in files
        }
    else:
        modules = {
            get_site_name(i): importlib.import_module('{}.{}'.format(module_path, i.split('.py')[0]))
            for i in files
        }
    spiders_dicts = {k: getattr(v, '__dict__') for k, v in modules.items()}
    return {k: i for k, v in spiders_dicts.items() for i in v.values() if valid(i)}


def args(func):
    # 转换只支持前端交互json格式
    def wrapper(self, *args, **kwargs):
        full_args_spec = getfullargspec(func)
        # 暂只支持 int str 抓换
        kwargs = dict()
        for index, arg in enumerate(full_args_spec.args[1:]):  # args=['self', 'way'] 切片是为了去掉self
            # 前端传过来的参数
            arg_from_front = self.get_body_argument(arg, '')
            # 手动写了注解
            annotation = full_args_spec.annotations.get(arg, None)
            if annotation:
                if arg_from_front:  # 前端已经传参数
                    if issubclass(annotation, (int, float, str)):
                        # print('*' * 8, arg_from_front)
                        v = annotation(arg_from_front)
                    elif isinstance(annotation, list):
                        v = self.get_body_arguments(arg, [])
                    else:  # 未知类型的, 统一是str
                        v = arg_from_front
                else:  # 前端参数为空,取注解默认值
                    # print(full_args_spec.defaults)
                    v = full_args_spec.defaults[index]
                    # print('-' * 8, v)
            else:  # 参数没写注解的，入参都是默认str
                v = arg_from_front
            kwargs[arg] = v
        # print(kwargs)
        return func(self, *args, **kwargs)

    return wrapper


# 校验key是否合法
def sec_check(func):
    def sec_check_wrapper(self, *args, **kwargs):
        sec_key = self.get_body_argument('key', '')
        if sec_key not in SEC_KEYS:
            self.finish({'msg': 'key error, please check!'})
            return
        return func(self, *args, **kwargs)

    return sec_check_wrapper


if __name__ == '__main__':
    pass
