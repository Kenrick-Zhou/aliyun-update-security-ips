from datetime import datetime

import requests
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_r_kvstore20150101 import models as r_kvstore_20150101_models
from alibabacloud_r_kvstore20150101.client import Client as RKvstore20150101Client
from alibabacloud_rds20140815 import models as rds_20140815_models
from alibabacloud_rds20140815.client import Client as Rds20140815Client
from alibabacloud_tea_util import models as util_models

from init import (
    CFG_DNS,
    CFG_RDS_A,
    CFG_RDS_M,
    CFG_TAIR_A,
    CFG_TAIR_M,
    CFG_URL,
    aliyun_config,
    logdebug,
    logerr,
    loginfo,
)


# 获取IP
def get_ip():
    ip = None
    for url in CFG_URL:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                ip = r.text.strip()
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 当前IP：{ip} URL：{url}")
                break
        except Exception:
            pass

    if ip is None:
        print("!!!!!!获取当前IP为空，可能断网!!!!!!")
        logerr("Cannot get IP, Check your network!!!!!")
        # pushdeer_md('# ⚠️断网⚠️')
    else:
        logdebug(ip)

    return ip


def update_rds(ip):
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = "rds.aliyuncs.com"
    client = Rds20140815Client(aliyun_config)
    runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)

    for instance in CFG_RDS_A["DBInstanceIds"]:
        try:
            r = client.describe_dbinstance_iparray_list_with_options(
                rds_20140815_models.DescribeDBInstanceIPArrayListRequest(dbinstance_id=instance), runtime
            )
            for i in r.body.items.dbinstance_iparray:
                if i.dbinstance_iparray_name == CFG_RDS_A["ArrayName"]:
                    if i.security_iplist != ip:
                        client.modify_security_ips_with_options(
                            rds_20140815_models.ModifySecurityIpsRequest(
                                dbinstance_id=instance, security_ips=ip, dbinstance_iparray_name=CFG_RDS_A["ArrayName"]
                            ),
                            runtime,
                        )
                        is_changed = True
                        loginfo(f'RDS IP白名单分组{CFG_RDS_A["ArrayName"]}成功修改为：{ip}')
                        print(f'RDS IP白名单分组{CFG_RDS_A["ArrayName"]}成功修改为：{ip}')
                    else:
                        break
        except Exception as e:
            logerr(f'RDS IP白名单分组{CFG_RDS_A["ArrayName"]}修改失败，错误信息：{e}')
            print(f'RDS IP白名单分组{CFG_RDS_A["ArrayName"]}修改失败，错误信息：{e}')
    return is_changed


def update_rds_manual_one_times(ip):
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = "rds.aliyuncs.com"
    client = Rds20140815Client(aliyun_config)
    runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)

    for instance in CFG_RDS_M["DBInstanceIds"]:
        try:
            r = client.describe_dbinstance_iparray_list_with_options(
                rds_20140815_models.DescribeDBInstanceIPArrayListRequest(dbinstance_id=instance), runtime
            )
            for i in r.body.items.dbinstance_iparray:
                if i.dbinstance_iparray_name == CFG_RDS_M["ArrayName"]:
                    if i.security_iplist != ip:
                        client.modify_security_ips_with_options(
                            rds_20140815_models.ModifySecurityIpsRequest(
                                dbinstance_id=instance, security_ips=ip, dbinstance_iparray_name=CFG_RDS_M["ArrayName"]
                            ),
                            runtime,
                        )
                        is_changed = True
                        loginfo(f'RDS IP白名单分组{CFG_RDS_M["ArrayName"]}成功修改为：{ip}')
                        print(f'RDS IP白名单分组{CFG_RDS_M["ArrayName"]}成功修改为：{ip}')
                    else:
                        break
        except Exception as e:
            logerr(e.message)
    return is_changed


def update_dns(ip):
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = "alidns.cn-hongkong.aliyuncs.com"
    client = Alidns20150109Client(aliyun_config)

    # 查询所有域名
    for domain in CFG_DNS:
        domain_name = list(domain.keys())[0]
        domain_rr_list = domain[domain_name]

        for rr in domain_rr_list:
            try:
                r = client.describe_domain_records_with_options(
                    alidns_20150109_models.DescribeDomainRecordsRequest(
                        domain_name=domain_name, key_word=rr, type="A", search_mode="EXACT"
                    ),
                    util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000),
                )
                record = r.body.domain_records.record[0]
                if record.value != ip:
                    client.update_domain_record_with_options(
                        alidns_20150109_models.UpdateDomainRecordRequest(
                            record_id=record.record_id, rr=record.rr, type=record.type, value=ip
                        ),
                        util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000),
                    )
                    is_changed = True
                    loginfo(f"{rr}.{domain_name}的记录值成功修改为：{ip}")
                    print(f"{rr}.{domain_name}的记录值成功修改为：{ip}")

                # else:
                #     break
            except Exception as e:
                logerr(f"{rr}.{domain_name}的记录值修改失败，错误信息：{e}")
                print(f"{rr}.{domain_name}的记录值修改失败，错误信息：{e}")  # 打印错误信息
    return is_changed


def update_tair(ip):
    """更新 Tair (Redis) 实例的安全IP白名单"""
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = "r-kvstore.aliyuncs.com"
    client = RKvstore20150101Client(aliyun_config)
    runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)

    for instance in CFG_TAIR_A["InstanceIds"]:
        try:
            # 查询当前安全IP白名单
            r = client.describe_security_ips_with_options(
                r_kvstore_20150101_models.DescribeSecurityIpsRequest(instance_id=instance), runtime
            )

            # 检查指定白名单分组的IP是否需要更新
            current_ips = None
            for group in r.body.security_ip_groups.security_ip_group:
                if group.security_ip_group_name == CFG_TAIR_A["GroupName"]:
                    current_ips = group.security_ip_list
                    break

            if current_ips != ip:
                # 修改安全IP白名单
                client.modify_security_ips_with_options(
                    r_kvstore_20150101_models.ModifySecurityIpsRequest(
                        instance_id=instance, security_ips=ip, security_ip_group_name=CFG_TAIR_A["GroupName"]
                    ),
                    runtime,
                )
                is_changed = True
                loginfo(f'Tair 安全IP白名单分组 {CFG_TAIR_A["GroupName"]} 成功修改为：{ip}')
                print(f'Tair 安全IP白名单分组 {CFG_TAIR_A["GroupName"]} 成功修改为：{ip}')
            else:
                print(f'Tair 实例 {instance} 的安全IP白名单分组 {CFG_TAIR_A["GroupName"]} 已是最新IP：{ip}')
        except Exception as e:
            logerr(f'Tair 安全IP白名单分组 {CFG_TAIR_A["GroupName"]} 修改失败，错误信息：{e}')
            print(f'Tair 安全IP白名单分组 {CFG_TAIR_A["GroupName"]} 修改失败，错误信息：{e}')
    return is_changed


def update_tair_manual_one_times(ip):
    """手动更新 Tair (Redis) 实例的安全IP白名单"""
    # 是否修改了IP
    is_changed = False

    # 访问的域名
    aliyun_config.endpoint = "r-kvstore.aliyuncs.com"
    client = RKvstore20150101Client(aliyun_config)
    runtime = util_models.RuntimeOptions(read_timeout=5000, connect_timeout=3000)

    for instance in CFG_TAIR_M["InstanceIds"]:
        try:
            # 查询当前安全IP白名单
            r = client.describe_security_ips_with_options(
                r_kvstore_20150101_models.DescribeSecurityIpsRequest(instance_id=instance), runtime
            )

            # 检查指定白名单分组的IP是否需要更新
            current_ips = None
            for group in r.body.security_ip_groups.security_ip_group:
                if group.security_ip_group_name == CFG_TAIR_M["GroupName"]:
                    current_ips = group.security_ip_list
                    break

            if current_ips != ip:
                # 修改安全IP白名单
                client.modify_security_ips_with_options(
                    r_kvstore_20150101_models.ModifySecurityIpsRequest(
                        instance_id=instance, security_ips=ip, security_ip_group_name=CFG_TAIR_M["GroupName"]
                    ),
                    runtime,
                )
                is_changed = True
                loginfo(f'Tair 安全IP白名单分组 {CFG_TAIR_M["GroupName"]} 成功修改为：{ip}')
                print(f'Tair 安全IP白名单分组 {CFG_TAIR_M["GroupName"]} 成功修改为：{ip}')
            else:
                print(f'Tair 实例 {instance} 的安全IP白名单分组 {CFG_TAIR_M["GroupName"]} 已是最新IP：{ip}')
        except Exception as e:
            logerr(f'Tair 安全IP白名单分组 {CFG_TAIR_M["GroupName"]} 修改失败，错误信息：{e}')
            print(f'Tair 安全IP白名单分组 {CFG_TAIR_M["GroupName"]} 修改失败，错误信息：{e}')
    return is_changed


if __name__ == "__main__":
    # update_rds(CFG_RDS_M['DBInstanceIds'], CFG_RDS_M['ArrayName'])
    # update_dns('8.8.8.8')

    # 手动更新一次RDS
    update_rds_manual_one_times(get_ip())

    # 手动更新一次Tair
    # update_tair_manual_one_times(get_ip())
