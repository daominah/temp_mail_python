import time
import datetime

if __name__ == "__main__":
    beginT = time.time()
    lastRefresh = time.time()
    print("beginT: %s, %s" % (beginT, datetime.datetime.now().isoformat()))
    while True:
        time.sleep(1)
        if (time.time() - lastRefresh) > 2:
            print(datetime.datetime.now().isoformat())
            lastRefresh = time.time()
