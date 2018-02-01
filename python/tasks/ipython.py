import re




line =('router uptime is 15 days, 8 hours, 32 minutes')
#match = re.search('System image file is (?P<image>\D.+)',line)
#print (match.group('image'))

#match = re.search('router uptime is (?P<uptime>\d.+)',line)
#match = re.search('Version         (?P<ios>\S+)' ,line)
#print (match.group('uptime'))

match = re.search('router uptime is (?P<uptime>\d.+)',line)
uptime = match.group('uptime')
print (uptime)