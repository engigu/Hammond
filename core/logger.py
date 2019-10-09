import sys


def get_logger():
    import logging
    fmt = logging.Formatter(
        '[%(way)s] - %(asctime)s - %(filename)s[%(funcName)s:%(lineno)d] - %(levelname)s: %(message)s')
    h_console = logging.StreamHandler(sys.stdout)
    h_console.setFormatter(fmt)
    logger = logging.getLogger('celery_senders')
    logger.setLevel(logging.INFO)
    logger.addHandler(h_console)
    return logger
