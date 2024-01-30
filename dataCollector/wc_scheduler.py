import schedule
import time
import os

def execute_bus() :
    os.system("python wc_seoul_bus.py")

execute_bus()
schedule.every(30).minutes.do(execute_bus)

while True:
    schedule.run_pending()
    time.sleep(1)