import os
import time
import logging.handlers
from contextlib import contextmanager
from functools import wraps

import yaml
from pypushdeer import PushDeer
from alibabacloud_tea_openapi import models as open_api_models

############################################
# 读取配置文件
yamlPath = f'{os.path.split(os.path.realpath(__file__))[0]}/config.yml'
with open(yamlPath, 'rb') as f:
    _config = yaml.safe_load(f)
    CFG_ALY = _config['Aliyun']
    CFG_INTERVAL = _config['check_interval']
    CFG_DNS = _config['DNS']['Domain_and_RR']
    CFG_RDS_A = _config['RDS']['AutoUpdate']
    CFG_RDS_M = _config['RDS']['ManualUpdate']
    CFG_URL = _config['IPCheckList']
    CFG_PUSHDEER = _config['PushDeer']
    CFG_LOG = _config['log']


############################################
# 可以跑几次测下自己的网络环境哪个访问速度会快些
# for url in CFG_URL:
#     r = requests.get(url, timeout=10)
#     print('{:<36} {:>16} {:>15}'.format(url, r.text.strip(), str(r.elapsed)))


############################################
# 阿里云Aliyun的配置
aliyun_config = open_api_models.Config(access_key_id=CFG_ALY['AK'], access_key_secret=CFG_ALY['SK'])


############################################
# 配置日志
# 日志目录初始化
os.makedirs(os.path.expanduser(CFG_LOG['path_dir']), exist_ok=True)
# 基础日志配置
logging.Formatter.converter = time.localtime
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s %(levelname)s %(name)s: \n%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

#######################
# INFO日志配置
info_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.expanduser(CFG_LOG['path_info']), when='D', interval=1, backupCount=90,
)
info_handler.suffix = '%Y%m%d.log'
info_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
info_handler.setFormatter(info_formatter)
logger_info = logging.getLogger('loginfo')
logger_info.setLevel(logging.INFO)
logger_info.addHandler(info_handler)


def loginfo(msg, *args, **kwargs): logger_info.info(msg, *args, **kwargs)


#######################
# ERROR日志配置
err_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.expanduser(CFG_LOG['path_err']), when='D', interval=1, backupCount=90,
)
err_handler.suffix = '%Y%m%d.log'
err_formatter = logging.Formatter('%(asctime)s %(levelname)s: ' + '=' * 13 + '!!! %(message)s !!!' + '=' * 13)
err_handler.setFormatter(err_formatter)
logger_err = logging.getLogger('err')
logger_err.setLevel(logging.ERROR)
logger_err.addHandler(err_handler)


def logerr(msg, *args, **kwargs): logger_err.error(msg, *args, **kwargs)


#######################
# Debug日志配置
logger_debug = logging.getLogger(f'({os.getpid()})debug🙂🤔🧐😱🤦🏻‍️🕵🏻‍️👨🏻‍🔧👨🏻‍🏭👨🏻‍💻💁🏻‍️🤫🤐😎🙂debug')
logger_debug.setLevel(logging.DEBUG)


def logdebug(msg, *args, **kwargs): logger_debug.debug(msg, *args, **kwargs)


#########################################################################
# 我们有两种方式来实现在pushdeer_md执行前去除代理，并在执行后恢复代理
# 下面是方法一：
# 我们将相关功能封装在一个上下文管理器（contextmanager）中，
# 这样就可以使用with子句来简化代码并复用功能
#########################################################################
@contextmanager
def no_proxy():
    http_proxy = os.environ.pop("http_proxy", None)
    https_proxy = os.environ.pop("https_proxy", None)
    os.environ.pop("HTTP_PROXY", None)
    os.environ.pop("HTTPS_PROXY", None)

    try:
        yield
    finally:
        if http_proxy:
            os.environ["http_proxy"] = http_proxy
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["https_proxy"] = https_proxy
            os.environ["HTTPS_PROXY"] = https_proxy


# def pushdeer_md(title, content=None):
#     pushdeer = PushDeer(pushkey=PUSHDEER_KEY)
#
#     with no_proxy():
#         pushdeer.send_markdown(text=title, desp=content)


#########################################################################
# 下面是方法二：
# 使用装饰器（decorator）来实现，这样可以对任意函数进行装饰
#########################################################################
def without_proxy(func):
    def clean_proxy():
        http_proxy = os.environ.pop("http_proxy", None)
        https_proxy = os.environ.pop("https_proxy", None)
        os.environ.pop("HTTP_PROXY", None)
        os.environ.pop("HTTPS_PROXY", None)

        return http_proxy, https_proxy

    def restore_proxy(http_proxy, https_proxy):
        if http_proxy:
            os.environ["http_proxy"] = http_proxy
            os.environ["HTTP_PROXY"] = http_proxy
        if https_proxy:
            os.environ["https_proxy"] = https_proxy
            os.environ["HTTPS_PROXY"] = https_proxy

    @wraps(func)
    def wrapper(*args, **kwargs):
        http_proxy, https_proxy = clean_proxy()
        try:
            result = func(*args, **kwargs)
        finally:
            restore_proxy(http_proxy, https_proxy)

        return result

    return wrapper


############################################
# 初始化PushDeer能力（可选，网络断掉时通知用，换别的也行）
pushdeer = PushDeer(pushkey=CFG_PUSHDEER['key']['network'])
@without_proxy
def pushdeer_md(title, content=None): pushdeer.send_markdown(text=title, desp=content)
