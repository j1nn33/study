#!/usr/bin/env python
"""
Проверка TCP - порта

"""
import socket
import re
import sys


def check_server(address, port):
    #Создать сокет TCP
    s = socket.socket()
    print ("Attempting to connect to %s on port %s" % (address, port))

    try:
        s.connect((address, port))
        print("Connected to %s on port %s" % (address, port))
        return True
    except socket.error:
        print ("Connection to %s on port %s failed " % (address, port))
        return False


def check_webserver(address, port, resource):

    #Создать строку запроса HTTP
    if not resource.startswith('/'):
        resource = '/' + resource
    request_string = "GET %s HTTP/1.1\r\nHost:%s\r\n\r\n" % (resource, address)
    print ('HTTP request:')
    print ('%s' % request_string)
    print (' ====RESULT============= ')
    #Создать сокет TCP
    s = socket.socket()
    print ("Attempting to connect to %s on port %s" % (address, port))

    try:
        s.connect((address, port))
        print ("Connected to %s on port %s" % (address, port))
        #print ('================')
        #print (type(request_string))
        #print('================')
        bytestring = request_string.encode('utf-8')   # перевод в байты
        s.send(bytestring)
        #Нам достаточно получить только первые 100 байтов
        rsp = s.recv(100).decode('utf-8')             # перевод в строку

        print ('Received 100 bytes of HTTP response')
        print ('%s' % rsp)
    except socket.error:
        print ("Connection to %s on port %s failed " % (address, port))
        return False
    finally:
        # закроем соединение
        print("Closing the connection")
        s.close()

    print ('')
    print ('====PARSING ======')
    lines = rsp.splitlines()
    print('First line of HTTP response: %s' % lines[1])
    try:
        version, status, message = re.split(r'\s+', lines[0], 2)
        print('Version: %s, Status: %s, Message: %s' % (version, status, message))
    except ValueError:
        print('Failed to split status line')
        return False
    if status in ['200', '301']:
        print('Success - status was %s' % status)
        print('WEB-page is OK')
        return True
    else:
         print('Status was %s' % status)
         print('WEB-page not found')
         return False


if __name__ == '__main__':
    # закоментирован кусок который позволяет задать параметры при запуске скрипта вручную
    """
    
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a", "--address", dest="address", default='localhost',
                      help="ADDRESS for server", metavar="ADDRESS")
    parser.add_option("-p", "--port", dest="port", type="int", default=80,
                      help="PORT for server", metavar="PORT")
    (options, args) = parser.parse_args()
    print ('options: %s, args: %s' % (options, args))
    """
    #address = '192.168.40.72'
    address = '192.168.40.3'
    port = 80
    resource = 'apache2-default'
    #resource = '/squid.eureca-corp.ru/accessdenied.gif'
    #check = check_server(options.address, options.port)
    print (' -----TESTINT CONNECTION----- ')
    check = check_server( address,port)
    print ('check_server returned %s' % check)
    print (' ')
    print (' -----TESTING WEB SERVICE----- ')
    web_check=check_webserver(address, port, resource)
    print ('check_webserver returned %s' % check)
    sys.exit(not check)