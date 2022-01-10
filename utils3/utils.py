#!/usr/bin/env python3

import time
def wait_until(func, parsms, timeout=10):
    waittime = 0
    while (1):
        try:
            print ('try:', waittime)
            func(*parsms)
        except Exception as e:
            waittime += 1
            time.sleep(1)
            if waittime >= timeout:
                return -1
            continue
        return waittime

    return waittime
