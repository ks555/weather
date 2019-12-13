from datetime import datetime
from apscheduler.scheduler import Scheduler
import time
import sys
import os
from weather.yr_forecast import YrForecast

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Start the scheduler
sched = Scheduler()
sched.start()

# Define the function that is to be executed
def my_job():
    YrForecast("cu", "romanian")

# The job will be executed on November 6th, 2009
# exec_date = datetime(2019, 12, 10, 11, 51, 0)

# Store the job in a variable in case we want to cancel it
job = sched.add_date_job(my_job, exec_date, args=['printing'])


while True:
    time.sleep(10)
sched.shutdown()