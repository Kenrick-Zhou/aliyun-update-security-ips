# aliyun-update-security-ips
自动定期（或手动）更新阿里云Aliyun RDS的IP白名单

方便DDNS环境下的服务器访问 或个人在外的访问，兼顾安全和便捷

_暂时只做了RDS的，能用，还比较简单就没做太多封装。
欢迎改造共建。_


## 用法
* update.py 手动运行，更新一次。用于笔记本电脑带在外面需要访问时使用
* updated.py 后台运行，自动定期检查更新白名单IP，用于在家的服务器（等DDNS环境）使用

### 配置文件

```yaml
Aliyun:
  AK: xxx  # Access Key ID
  SK: xxx  # Access Key Secret

RDS:
  AutoUpdate:  # 自动定时更新配置
    ArrayName: home  # 白名单分组名称（要提前创建好）
    Interval: 1000  # 间隔多少秒检查一次
    DBInstanceIds: &all_instance  # 要修改的RDS实例ID
      - rm-xxx
  ManualUpdate:  # 手动更新配置
    ArrayName: my
    DBInstanceIds: # 要修改的RDS实例ID
      *all_instance

IPCheckList:  # 查看本机公网IP的网址
  - https://ip.clang.cn/
  - http://icanhazip.com
  - https://ipecho.net/plain
  - http://whatismyip.akamai.com/
  - https://tnx.nl/ip
  - https://www.trackip.net/ip
  - http://ip.cip.cc/

PushDeer:  # 给手机发推送用的，可忽略（需自行删除两行代码）
  key:
    network: xxx

log:  # 日志存放位置（会自动创建相应目录）
  path_info: ~/log/aliyun-update-security-ips/info
  path_err: ~/log/aliyun-update-security-ips/err
```

