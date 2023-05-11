import time

from update import *
from init import loginfo

if __name__ == '__main__':
    loginfo('service started.')
    while True:
        ip = get_ip()
        if ip is not None:
            is_update_rds = update_rds(ip)
            is_update_dns = update_dns(ip)
            if is_update_rds or is_update_dns:
                pushdeer_md(f'# 🔃IP🔃 {ip}', f'{CFG_DNS}\n\n{CFG_RDS_A}')
        loginfo(f'one loop over, will sleep {CFG_INTERVAL}s')
        time.sleep(CFG_INTERVAL)

