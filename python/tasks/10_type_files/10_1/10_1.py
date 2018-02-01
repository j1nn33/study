# -*- coding: utf-8 -*-
"""
Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

Для выполнения задания нужно создать две функции.

    Функция parse_sh_version:
        * ожидает аргумент output в котором находится вывод команды sh version (не имя файла)
        * обрабатывает вывод, с помощью регулярных выражений
        * возвращает кортеж из трёх элементов:
                * ios - в формате "12.4(5)T"
                * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
                * uptime - в формате "5 days, 3 hours, 3 minutes"

    Функция write_to_csv:  ожидает два аргумента:
        * имя файла, в который будет записана информация в формате CSV
                * данные в виде списка списков, где:
                * первый список - заголовки столбцов,
                * остальные списки - содержимое
                * функция записывает содержимое в файл, в формате CSV и ничего не возвращает
                (В файле routers_inventory.csv должны быть такие столбцы:
                                    * hostname, ios, image, uptime)

   Остальное содержимое скрипта может быть в скрипте, а может быть в ещё одной функции.

   В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
   Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

   Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv

sh_version_files = glob.glob('sh_vers*')    # получение списка файлов в каталоге
list_of_file = sh_version_files             # хранит имена файлов исходников в списке

headers = ['hostname', 'ios', 'image', 'uptime']
#################################################################################################
# читает файлы и передает результат в виде списка 
def read_file (file_name):
    temp_list=[]    
    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list
#################################################################################################
# обрабатывает вывод, с помощью регулярных выражений и возвращает кортеж
def parse_sh_version (input_date):
    list_keys = []
    temp_tuple = ()
    for line in input_date:
        if  line.startswith('Cisco IOS Software'):
            match = re.search('Version (?P<ios>\S+)' ,line)
            ios = match.group('ios')[0:-1:]
            #print (match.group('ios')[0:-1:])
        elif line.startswith('router uptime is'):
            match = re.search('router uptime is (?P<uptime>\d.+)',line)
            uptime = match.group('uptime')
            #print (match.group('uptime'))
        elif line.startswith('System image file is'):
            match = re.search('System image file is (?P<image>\D.+)',line)
            image = match.group('image')[1:-1:]
            #print (match.group('image'))
        else:
            pass
    list_keys.append (ios)
    list_keys.append (image)
    list_keys.append (uptime)
    #print (list_keys)
    temp_tuple = tuple(list_keys)
    #print (temp_tuple)
    return temp_tuple
#################################################################################################
# получает имя файла (в качестве элемента списка list_of_file  )
def host_name(item_list_of_file):
    host_nm = item_list_of_file[11:13:]
    return host_nm
#################################################################################################
# собирает файлы для отправки в функцию записи
def collect_data(input_tuple, device_name):
    """собирает строку вида
    ['r2', '12.4(4)T', '"disk0:c7200-js-mz.124-4.T"', '45 days, 8 hours, 22 minutes']
    """
    import_cvs = []
    import_cvs.append (device_name)
    for i in input_tuple:
        import_cvs.append (i)
    return import_cvs
#################################################################################################
# записывает информацию в файл
def write_to_csv (name, input_write_data):
    with open(name, 'w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in input_write_data:
            writer.writerow(row)
    with open(name) as f:
        print(f.read())

    return 

#################################################################################################
if __name__ == '__main__':
    import_cvs =[]
    import_cvs.append(headers)
    
    for device in list_of_file:
        
        temp_list_from_file=[]
        temp_list_from_collect_data=[]
        temp_tuple=()
       
        device_name=host_name(device)
        temp_list_from_file = read_file ('/home/ubuntu/workspace/python/tasks/10_type_files/10_1/'+device)
        temp_tuple=parse_sh_version(temp_list_from_file)
        temp_list_from_collect_data = collect_data (temp_tuple, device_name)
        import_cvs.append(temp_list_from_collect_data)
    
    write_file = '/home/ubuntu/workspace/python/tasks/10_type_files/10_1/routers_inventory.csv'
    write_to_csv (write_file, import_cvs)  
        
      