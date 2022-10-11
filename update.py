import requests
from alibabacloud_rds20140815 import models as rds_20140815_models

from init import *


def update(db_instances_ids, array_name):
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
        pushdeer_md('⚠️断网⚠️')
    else:
        logdebug(ip)

    for instance in db_instances_ids:
        try:
            r = client.describe_dbinstance_iparray_list_with_options(
                rds_20140815_models.DescribeDBInstanceIPArrayListRequest(dbinstance_id=instance),
                runtime
            )
            for i in r.body.items.dbinstance_iparray:
                if i.dbinstance_iparray_name == array_name:
                    if i.security_iplist != ip:
                        rsp = client.modify_security_ips_with_options(
                            rds_20140815_models.ModifySecurityIpsRequest(
                                dbinstance_id=instance,
                                security_ips=ip,
                                dbinstance_iparray_name=array_name
                            ),
                            runtime
                        )
                        loginfo(f'RDS IP白名单分组{array_name}成功修改为：{ip}')
                    else:
                        break
        except Exception as e:
            logerr(e.message)


if __name__ == '__main__':
    update(CFG_RDS_M['DBInstanceIds'], CFG_RDS_M['ArrayName'])
