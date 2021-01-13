#Convert spellbreak log timestamps strings to date_time value
import datetime

class_timestamp = '2021.01.11-18.16.01:674'
current_latest=datetime.datetime.strptime(class_timestamp, '%Y.%m.%d-%H.%M.%S:%f')

print('Date-time:', class_timestamp)

# get first 25 chars of string that has a match of one of the classes