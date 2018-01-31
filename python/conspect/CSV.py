"""CSV"""

# каждая строка файла - это строка таблицы. Но разделителем может быть не только запятая.
#   file - sw_data.csv
#   hostname,vendor,model,location
#   sw1,Cisco,3750,London
#   sw2,Cisco,3850,Liverpool

""" Чтение"""
import csv

with open('sw_data.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        
# ['hostname', 'vendor', 'model', 'location']
# ['sw1', 'Cisco', '3750', 'London']

with open('sw_data.csv') as f:
    reader = csv.reader(f)
    print(reader)

# <_csv.reader object at 0x10385b050>
    print(list(reader))
# [['hostname', 'vendor', 'model', 'location'], ['sw1', 'Cisco', '3750', 'London'], ['sw2', 'Cisco', '3850', 'Liverpool']]


# заголовки столбцов удобней получить отдельным объектом.
import csv
with open('sw_data.csv') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print('Headers: ', headers)
    for row in reader:
        print(row)
        
# получить словари: ключи - это названия столбцов, 
#                значения - значения столбцов.

# DictReader создает не стандартные словари Python, а упорядоченные словари. За счет
# этого порядок элементов соответствует порядку столбцов в CSV файле.

import csv
with open('sw_data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
        print(row['hostname'], row['model'])
        
#OrderedDict([('hostname', 'sw1'), ('vendor', 'Cisco'), ('model', '3750'), ('location', 'London')])
#sw1 3750
#OrderedDict([('hostname', 'sw2'), ('vendor', 'Cisco'), ('model', '3850'), ('location', 'Liverpool')])

"""Запись"""

import csv
data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f)
    for row in data:
        writer.writerow(row)
with open('sw_data_new.csv') as f:
    print(f.read())
    
# hostname,vendor,model,location
# sw1,Cisco,3750,"London, Best str"
# sw2,Cisco,3850,"Liverpool, Better str"
# sw3,Cisco,3650,"Liverpool, Better str"
# sw4,Cisco,3650,"London, Best str"

# строки в последнем столбце взяты в кавычки, а остальные значения - нет.
# Так получилось из-за того, что во всех строках последнего столбца есть запятая. И
# кавычки указывают на то, что именно является целой строкой. Когда запятая
# находятся в кавычках, модуль csv не воспринимает её как разделитель.

# Модуль csv позволяет управлять этим. Для того, чтобы все строки записывались в файл csv с кавычками

import csv
data = [['hostname', 'vendor', 'model', 'location'],
        ['sw1', 'Cisco', '3750', 'London, Best str'],
        ['sw2', 'Cisco', '3850', 'Liverpool, Better str'],
        ['sw3', 'Cisco', '3650', 'Liverpool, Better str'],
        ['sw4', 'Cisco', '3650', 'London, Best str']]

with open('sw_data_new.csv', 'w') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    for row in data:
        writer.writerow(row)
with open('sw_data_new.csv') as f:
    print(f.read())

# "hostname","vendor","model","location"
# "sw1","Cisco","3750","London, Best str"
# "sw2","Cisco","3850","Liverpool, Better str"
# "sw3","Cisco","3650","Liverpool, Better str"
# "sw4","Cisco","3650","London, Best str"

"""DictWriter"""
# С помощью DictWriter можно записать словари в формат csv.
# В целом DictWriter работает так же, как writer, но так как словари не упорядочены, надо
# указывать явно в каком порядке будут идти столбцы в файле. Для этого используется
# параметр fieldnames (файл csv_write_dict.py):
import csv
data = [{'hostname': 'sw1',
         'location': 'London',
         'model': '3750',
         'vendor': 'Cisco'},
        {'hostname': 'sw2',
         'location': 'Liverpool',
         'model': '3850',
         'vendor': 'Cisco'},
        {'hostname': 'sw3',
         'location': 'Liverpool',
         'model': '3650',
         'vendor': 'Cisco'},
        {'hostname': 'sw4',
         'location': 'London',
         'model': '3650',
         'vendor': 'Cisco'}]
         
with open('csv_write_dictwriter.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=list(data[0].keys()), quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in data:
        writer.writerow(d)
        
        
# "vendor","location","hostname","model"
# "Cisco","London","sw1","3750"
# "Cisco","Liverpool","sw2","3850"
# "Cisco","Liverpool","sw3","3650"
# "Cisco","London","sw4","3650"


"""Указание разделителя"""

# hostname;vendor;model;location
# sw1;Cisco;3750;London
# sw2;Cisco;3850;Liverpool
# sw3;Cisco;3650;Liverpool
# sw4;Cisco;3650;London


import csv
with open('sw_data2.csv') as f:
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        print(row)