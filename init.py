import logging.handlers
import os
from contextlib import contextmanager
from functools import wraps

import requests
import yaml
from alibabacloud_tea_openapi import models as open_api_models
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

############################################
# 读取配置文件
yamlPath = f"{os.path.split(os.path.realpath(__file__))[0]}/config.yml"
with open(yamlPath, "rb") as f:
    _config = yaml.safe_load(f)
    # CFG_ALY = _config['Aliyun']
    CFG_INTERVAL = _config["check_interval"]
    CFG_DNS = _config["DNS"]["Domain_and_RR"]
    CFG_RDS_A = _config["RDS"]["AutoUpdate"]
    CFG_RDS_M = _config["RDS"]["ManualUpdate"]
    CFG_TAIR_A = _config.get("Tair", {}).get("AutoUpdate", {"GroupName": "default", "InstanceIds": []})
    CFG_TAIR_M = _config.get("Tair", {}).get("ManualUpdate", {"GroupName": "default", "InstanceIds": []})
    CFG_URL = _config["IPCheckList"]
    CFG_NOTIFICATION = _config.get("Notification", {"enabled": False, "type": "none"})
    CFG_LOG = _config["log"]


############################################
# 可以跑几次测下自己的网络环境哪个访问速度会快些
# for url in CFG_URL:
#     r = requests.get(url, timeout=10)
#     print('{:<36} {:>16} {:>15}'.format(url, r.text.strip(), str(r.elapsed)))


############################################
# 阿里云Aliyun的配置
aliyun_config = open_api_models.Config(access_key_id=os.getenv("ALY_AK"), access_key_secret=os.getenv("ALY_SK"))


############################################
# 配置日志
# 日志目录初始化
os.makedirs(os.path.expanduser(CFG_LOG["path_dir"]), exist_ok=True)
# 基础日志配置
# logging.Formatter.converter = time.localtime
# logging.basicConfig(
#     level=logging.WARNING,
#     format='%(asctime)s %(levelname)s %(name)s: \n%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
# )

#######################
# INFO日志配置
info_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.expanduser(CFG_LOG["path_info"]),
    when="D",
    interval=1,
    backupCount=90,
)
info_handler.suffix = "%Y%m%d.log"
info_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
info_handler.setFormatter(info_formatter)
logger_info = logging.getLogger("loginfo")
logger_info.setLevel(logging.INFO)
logger_info.addHandler(info_handler)


def loginfo(msg, *args, **kwargs):
    logger_info.info(msg, *args, **kwargs)


#######################
# ERROR日志配置
err_handler = logging.handlers.TimedRotatingFileHandler(
    os.path.expanduser(CFG_LOG["path_err"]),
    when="D",
    interval=1,
    backupCount=90,
)
err_handler.suffix = "%Y%m%d.log"
err_formatter = logging.Formatter("%(asctime)s %(levelname)s: " + "=" * 13 + "!!! %(message)s !!!" + "=" * 13)
err_handler.setFormatter(err_formatter)
logger_err = logging.getLogger("err")
logger_err.setLevel(logging.ERROR)
logger_err.addHandler(err_handler)


def logerr(msg, *args, **kwargs):
    logger_err.error(msg, *args, **kwargs)


#######################
# Debug日志配置
logger_debug = logging.getLogger(f"({os.getpid()})debug🙂🤔🧐😱🤦🏻‍️🕵🏻‍️👨🏻‍🔧👨🏻‍🏭👨🏻‍💻💁🏻‍️🤫🤐😎🙂debug")
logger_debug.setLevel(logging.DEBUG)


def logdebug(msg, *args, **kwargs):
    logger_debug.debug(msg, *args, **kwargs)


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
# 通知功能（可选，网络断掉时通知用）
class BarkNotifier:
    """Bark 推送通知"""

    def __init__(self, server_url):
        self.server_url = server_url.rstrip("/")

    def send(self, title, content=None):
        """发送 Bark 通知

        Args:
            title: 通知标题
            content: 通知内容（可选）
        """
        url = f"{self.server_url}/{title}"
        if content:
            url = f"{url}/{content}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logerr(f"Bark notification failed: {e}")
            return False


class PushDeerNotifier:
    """PushDeer 推送通知"""

    def __init__(self, pushkey):
        self.pushkey = pushkey
        self.api_url = "https://api2.pushdeer.com/message/push"

    def send(self, title, content=None):
        """发送 PushDeer 通知

        Args:
            title: 通知标题
            content: 通知内容（可选）
        """
        try:
            params = {"pushkey": self.pushkey, "text": title, "type": "markdown"}
            if content:
                params["desp"] = content

            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            return True
        except Exception as e:
            logerr(f"PushDeer notification failed: {e}")
            return False


# 初始化通知器
_notifier = None
if CFG_NOTIFICATION.get("enabled", False):
    notification_type = CFG_NOTIFICATION.get("type", "none").lower()

    if notification_type == "bark":
        bark_key = os.getenv("BARK_KEY")
        if bark_key:
            _notifier = BarkNotifier(bark_key)
        else:
            logerr("Bark notification enabled but BARK_KEY not found in .env")

    elif notification_type == "pushdeer":
        pushdeer_key = os.getenv("PUSHDEER_KEY")
        if pushdeer_key:
            _notifier = PushDeerNotifier(pushdeer_key)
        else:
            logerr("PushDeer notification enabled but PUSHDEER_KEY not found in .env")


@without_proxy
def send_notification(title, content=None):
    """发送通知（统一接口）

    Args:
        title: 通知标题
        content: 通知内容（可选）
    """
    if _notifier:
        return _notifier.send(title, content)
    return False


# 兼容旧代码的别名
def pushdeer_md(title, content=None):
    """已废弃：请使用 send_notification 替代"""
    return send_notification(title, content)
