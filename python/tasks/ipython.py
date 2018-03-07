import datetime 
from datetime import timedelta, datetime
#now = str(datetime.datetime.today().replace(microsecond=0))
#print('now ', type (now), now)

now = datetime.today().replace(microsecond=0)
week_ago = now - timedelta(days = 7)
day_ago = now - timedelta(days = 1)
print(now)
print(week_ago)
print(now > week_ago)
print(str(now) > str(week_ago))