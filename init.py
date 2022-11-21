import os
import time
import logging.handlers

import yaml
from pypushdeer import PushDeer
from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

############################################
# 读取配置文件
yamlPath = f'{os.path.split(os.path.realpath(__file__))[0]}/config.yml'
with open(yamlPath, 'rb') as f:
    config = yaml.safe_load(f)
    CFG_ALY = config['Aliyun']
    CFG_RDS_A = config['RDS']['AutoUpdate']
    CFG_RDS_M = config['RDS']['ManualUpdate']
    CFG_URL = config['IPCheckList']
    CFG_PUSHDEER = config['PushDeer']
    CFG_LOG = config['log']

############################################
# 初始化PushDeer能力（可选，网络断掉时通知用，换别的也行）
pushdeer = PushDeer(pushkey=CFG_PUSHDEER['key']['network'])
def pushdeer_md(title, content=None): pushdeer.send_markdown(text=title, desp=content)

############################################
# 可以跑几次测下自己的网络环境哪个访问速度会快些
# for url in CFG_URL:
#     r = requests.get(url, timeout=10)
#     print('{:<36} {:>16} {:>15}'.format(url, r.text.strip(), str(r.elapsed)))


############################################
# 阿里云Aliyun的配置
config = open_api_models.Config(access_key_id=CFG_ALY['AK'], access_key_secret=CFG_ALY['SK'])
# 访问的域名
config.endpoint = f'rds.aliyuncs.com'
client = Rds20140815Client(config)
runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)



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