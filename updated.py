import time

from init import CFG_DNS, CFG_INTERVAL, CFG_RDS_A, CFG_TAIR_A, loginfo, send_notification
from update import get_ip, update_dns, update_rds, update_tair

if __name__ == "__main__":
    loginfo("service started.")
    while True:
        ip = get_ip()
        if ip is not None:
            if update_rds(ip):
                send_notification(f"🔃RDS IP🔃 {ip}", f"{CFG_RDS_A}")
            if update_dns(ip):
                send_notification(f"🔃DNS IP🔃 {ip}", f"{CFG_DNS}")
            if update_tair(ip):
                send_notification(f"🔃Tair IP🔃 {ip}", f"{CFG_TAIR_A}")
        loginfo(f"one loop over, will sleep {CFG_INTERVAL}s")
        time.sleep(CFG_INTERVAL)
