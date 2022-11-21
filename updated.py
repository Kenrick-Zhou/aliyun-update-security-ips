import time

from update import update
from init import CFG_RDS_A, loginfo

if __name__ == '__main__':
    loginfo('service started.')
    while True:
        update(CFG_RDS_A['DBInstanceIds'], CFG_RDS_A['ArrayName'])
        time.sleep(CFG_RDS_A['Interval'])
        loginfo('one loop over')
