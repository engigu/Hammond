import importlib
import inspect
import os

from senders.base_sender import BaseSender as Base


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

    module_file_path = os.path.join(base_path, os.sep.join(module_path.split('.')))
    files = [i for i in os.listdir(module_file_path) if i.startswith(prefix)]
    modules = {get_site_name(i): importlib.import_module('{}.{}'.format(module_path, i.split('.py')[0]))
               for i in files}
    spiders_dicts = {k: getattr(v, '__dict__') for k, v in modules.items()}
    return {k: i for k, v in spiders_dicts.items() for i in v.values() if valid(i)}


if __name__ == '__main__':

    pass
