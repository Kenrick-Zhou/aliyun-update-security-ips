import requests
from alibabacloud_tea_util import models as util_models
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client


from init import *


# 获取IP
def get_ip():
    ip = None
    for url in CFG_URL:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                ip = r.text.strip()
                break
        except:
            pass

    if ip is None:
        logerr('Cannot get IP, Check your network!')
        pushdeer_md('# ⚠️断网⚠️')
    else:
        logdebug(ip)

    return ip


def update_rds(ip):
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = f'rds.aliyuncs.com'
    client = Rds20140815Client(aliyun_config)
    runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)

    for instance in CFG_RDS_A['DBInstanceIds']:
        try:
            r = client.describe_dbinstance_iparray_list_with_options(
                rds_20140815_models.DescribeDBInstanceIPArrayListRequest(dbinstance_id=instance),
                runtime
            )
            for i in r.body.items.dbinstance_iparray:
                if i.dbinstance_iparray_name == CFG_RDS_A['ArrayName']:
                    if i.security_iplist != ip:
                        rsp = client.modify_security_ips_with_options(
                            rds_20140815_models.ModifySecurityIpsRequest(
                                dbinstance_id=instance,
                                security_ips=ip,
                                dbinstance_iparray_name=CFG_RDS_A['ArrayName']
                            ),
                            runtime
                        )
                        is_changed = True
                        loginfo(f'RDS IP白名单分组{CFG_RDS_A["ArrayName"]}成功修改为：{ip}')
                    else:
                        break
        except Exception as e:
            logerr(e.message)
    return is_changed


def update_dns(ip):
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = f'alidns.cn-hongkong.aliyuncs.com'
    client = Alidns20150109Client(aliyun_config)

    # 查询所有域名
    for domain in CFG_DNS:
        domain_name = list(domain.keys())[0]
        domain_rr_list = domain[domain_name]

        for rr in domain_rr_list:
            try:
                r = client.describe_domain_records_with_options(
                    alidns_20150109_models.DescribeDomainRecordsRequest(
                        domain_name=domain_name,
                        rrkey_word=rr
                    ),
                    util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)
                )
                record = r.body.domain_records.record[0]
                if record.value != ip:
                    rsp = client.update_domain_record_with_options(
                        alidns_20150109_models.UpdateDomainRecordRequest(
                            record_id=record.record_id,
                            rr=record.rr,
                            type=record.type,
                            value=ip
                        ),
                        util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)
                    )
                    is_changed = True
                    loginfo(f'{rr}.{domain_name}的记录值成功修改为：{ip}')

                # else:
                #     break
            except Exception as e:
                logerr(e.message)
    return is_changed

if __name__ == '__main__':
    # update_rds(CFG_RDS_M['DBInstanceIds'], CFG_RDS_M['ArrayName'])
    update_dns('8.8.8.8')
