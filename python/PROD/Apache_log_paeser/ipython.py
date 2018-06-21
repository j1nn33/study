"""
обкатка алгоритма регулярки

"""

import re
log_line_re = re.compile(r'''(?P<remote_host>\S+) #IP ADDRESS
                             \s+ #whitespace
                             \S+ #remote logname
                             \s+ #whitespace
                             \S+ #remote user
                             \s+ #whitespace
                             \[[^\[\]]+\] #time
                             \s+ #whitespace
                             "[^"]+" #first line of request
                             \s+ #whitespace
                             (?P<status>\d+)
                             \s+ #whitespace
                             (?P<bytes_sent>-|\d+)
                             \s* #whitespace
                             ''', re.VERBOSE)

line ='c-24-20-163-223.client.comcast.net - - [09/Mar/2004:13:14:53 -0800] "GET / HTTP/1.1" 200 3169'

print (line)
m = log_line_re.match(line)
#print (m)
l = log_line_re.match(line).group()
print ('remote_host ', m.group('remote_host'))
print ('status ', m.group('status'))
print ('bytes_sent ', m.group('bytes_sent'))
print ('l ------',l)
if m:
    print ('YES')
    groupdict = m.groupdict()
    if groupdict['bytes_sent'] == '-':
        groupdict['bytes_sent'] = '0'
        print(groupdict)
else:
     print ('NO')
     groupdict ={'remote_host': None,
                 'status':None,
                 'bytes_sent':'0'
                  }
     print(groupdict)
