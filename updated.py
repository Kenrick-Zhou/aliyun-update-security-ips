import time

from update import *
from init import loginfo

if __name__ == '__main__':
    loginfo('service started.')
    while True:
        ip = get_ip()
        if ip is not None:
            if update_rds(ip):
                pushdeer_md(f'# 🔃RDS IP🔃 {ip}', f'{CFG_RDS_A}')
            if update_dns(ip):
                pushdeer_md(f'# 🔃DNS IP🔃 {ip}', f'{CFG_DNS}')
        loginfo(f'one loop over, will sleep {CFG_INTERVAL}s')
        time.sleep(CFG_INTERVAL)

