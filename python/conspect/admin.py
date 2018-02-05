""""
ДЛЯ СИСТЕМНОГО АДМИНИСТРАТРОВАНИЯ
"""""
"------------РАБОТА С ФАЙЛАМИ"
"""
'r' – открыть файл для чтения;
'w' – открыть файл для записи;
'x' – открыть файл с целью создания, если файл существует,
      то вызов функции open завершится с ошибкой;
'a' – открыть файл для записи, при этом новые 
      данные будут добавлены в конец файла, без удаления существующих;
'b' – бинарный режим;
't' – текстовый режим;
'+' – открывает файл для обновления

file.closed – возвращает true если файл закрыт 
              и false в противном случае;
file.mode   – возвращает режим доступа к файлу, 
              при этом файл должен быть открыт;
""" Получение пути файлов
import glob
# позволяет получить список фйлов в каталоге по маске


sh_version_files = glob.glob('sh_vers*')
print(sh_version_files)
# ['sh_version_r2.txt', 'sh_version_r3.txt', 'sh_version_r1.txt']


import os
print(os.getcwd())
# /home/ubuntu/workspace/python/tasks

#.  - данная папка
#.. - родительская папка 

import os
import getpass

# получение каталога где лежит файл path.py

p = os.path.dirname(__file__)
# D:/SOURCE/python/untitled/venv

# получение полного имени файла

l = os.path.join(os.path.dirname(__file__),'path.py')

# если файл находиться в папке folder которая находиться в этом каталоге
# D:/SOURCE/python/untitled/venv\folder\path.py True
s = os.path.join(os.path.dirname(__file__),'folder','path.py')

print(getpass.getuser())

print('-----------')
print (p)
# D:/SOURCE/python/untitled/venv\path.py True
print (l, os.path.exists(l))
print('-----------')



"""
    "ОТКРЫТИЕ И ЗАКРЫТИЕ ФАЙЛОВ"
f = open("test.txt", "r")
print("file.closed: " + str(f.closed))
"file.closed: False"
print("file.mode: " + f.mode)
"file.mode: r"
print("file.name: " + f.name)
"file.name: test.txt"

    "ЧТЕНИЕ ДАННЫХ ИЗ ФАЙЛА"

"read(размер) считывает из файла определенное количество символов"

f = open("test.txt", "r")
f.read()
"1 2 3 4 5 \n Work with file \n"
f.close()

f = open("test.txt", "r")
f.read(5)
"1 2 3"
f.close()

"Метод readline() позволяет считать строку из открытого файла."
f = open("test.txt", "r")
f.readline()
"1 2 3 4 5 \n""
f.close()

"Построчное считывание с помощью оператора for"
f = open("test.txt", "r")
for line in f:
    print (line)

"1 2 3 4 5"
"Work with file"
f.close()

    "ЗАПИСЬ ДАННЫХ В ФАЙЛ"

f = open("test.txt", "a")
f.write("Test string")
"11"
f.close()

"tell() возвращает текущую позицию “условного курсора” в файле."
f = open("test.txt", "r")
f.read(5)
'1 2 3'
f.tell()
"5"
f.close()

"Метод seek(позиция) выставляет позицию в файле."
"1 2 3 4 5"
f = open("test.txt", "r")
f.tell()
"0"
f.seek(8)
"8"
f.read(1)
"5"
f.tell()
"9"
f.close()

"""with при его использовании нет необходимости закрывать файл, 
при завершении работы с ним, эта операция будет выполнена автоматически."""

with open ("test.txt", "r") as f:
    for line in f:
    print(line)


"""1 2 3 4 5

Work with file
Test string"""
f.closed
True



