#!/bin/python3
#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
#----------------------------
# 
"""
ПОРЯДОК ИСПОЛЬЗОВАНИЯ:
apache_log_parser_split.py some_log_file
Этот сценарий принимает единственный аргумент командной строки: имя файла
журнала, который требуется проанализировать. Он анализирует содержимое файла
и генерирует отчет, содержащий перечень удаленных хостов и число байтов,
переданных каждому из них.
"""
import sys
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

""" старая версия функции основанная на извлечение информации при помощи разбиения строки пробелами"""

#def dictify_logline(line):
    #"""возвращает словарь, содержащий информацию, извлеченную из
    #комбинированного файла журнала
    #В настоящее время нас интересуют только адреса удаленных хостов
    #и количество переданных байтов, но для полноты картины мы
    #добавили выборку кода состояния.
    #АЛГОРИТМ
    #строка разбивается по пробелам
    #0             1 2 3                     4      5    6               7         8   9
    #200.222.33.33 - - [09/Mar/2004:11:21:36 -0800] "GET /AmavisNew.html HTTP/1.1" 200 2300
    #1-320.cnc.bc.ca - - [09/Mar/2004:11:43:54 -0800] "GET /ie.htm HTTP/1.1" 200 3518

    #"""
    #split_line = line.split()
    #return {'remote_host': split_line[0],
    #        'status': split_line[8],
    #        'bytes_sent': split_line[9],
    #        }

""" новая версия функции основанная на регулярном выражении"""
def dictify_logline(line):
    """возвращает словарь, содержащий информацию, извлеченную из
        комбинированного файла журнала
        В настоящее время нас интересуют только адреса удаленных хостов
        и количество переданных байтов, но для полноты картины мы
        добавили выборку кода состояния.
    """
    m = log_line_re.match(line)
    #print (m)
    #print('remote_host ', m.group('remote_host'))
    #print('status ', m.group('status'))
    #print('bytes_sent ', m.group('bytes_sent'))
    #print ('m - полученные совпадения  ',m)
    if m:
        groupdict = m.groupdict()
        if groupdict['bytes_sent'] == '-':
            groupdict['bytes_sent'] = '0'
            print ('  groupdict     ', groupdict)
        return groupdict
    else:
        """
        Если соответствие не было найдено, возвращается словарь с теми же 
        самыми ключами, но со значениями элементов, равными None и 0.
        """
        return {'remote_host': None,
                'status':None,
                'bytes_sent':'0'
                }


def generate_log_report(logfile):
    """возвращает словарь в формате:
       remote_host=>[список числа переданных байтов]
    Эта функция принимает объект типа file, выполняет обход всех строк
    в файле и создает отчет о количестве байтов, переданных при каждом
    обращении удаленного хоста к веб серверу.
    """
    report_dict = {}
    for line in logfile:
        line_dict = dictify_logline(line)
        print(line_dict)
        try:
            bytes_sent = int(line_dict['bytes_sent'])
        except ValueError:
            print("!!!!! - something wrong in field ['bytes_sent'] - rise exception")
            #полностью игнорировать непонятные нам ошибки
            continue
        report_dict.setdefault(line_dict['remote_host'], []).append(bytes_sent)

    return report_dict


def generate_sum_byte(log_report):
    """возвращает словарь в формате:
           remote_host=>[сумма переданных байтов]
        Эта функция принимает словарь в формате:
       remote_host=>[список числа переданных байтов]
        """
    report_sum = {}
    list_bytes_sent_from_host = []
    for key in log_report:
        list_bytes_sent_from_host = log_report[key]
        #print (list_bytes_sent_from_host)
        total_bytes_sent = sum(i for i in list_bytes_sent_from_host)
        #print(total_bytes_sent)
        report_sum [key] = total_bytes_sent

    return report_sum

if __name__ == "__main__":
    # проверка на наличие аргументов при запуске программы
    """"
    if not len(sys.argv) > 1:
        print(__doc__)
        sys.exit(1)
    infile_name = sys.argv[1]
    """

    infile_name = "/home/const/PycharmProjects/pyeng/access_log"

    try:
        infile = open(infile_name, 'r')
    except IOError:
        print("You must specify a valid file to parse")
        print(__doc__)
        sys.exit(1)

    log_report = generate_log_report(infile)
    print('#####################')

    print(log_report)
    print(' ')
    sum_byte = generate_sum_byte(log_report)
    print('#####################')
    print(sum_byte)

    infile.close()