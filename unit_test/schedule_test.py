import time

import schedule


def job():
    print("I'm working...")
    return 1


schedule.every().day.at("14:08").do(job)

while True:
    x = schedule.run_pending()
    time.sleep(0.05)
