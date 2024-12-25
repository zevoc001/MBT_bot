import schedule
import database as db
import time


def run():
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except:
            break


