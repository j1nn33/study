"""открытие/закрытие
   чтение
   запись
   Закрытие файлов
   whith    -    актуально 
"""

"""with 
"""

# конструкция with гарантирует закрытие файла автоматически
# 
#  ./file.txt фал лежит в той же папке. 
# ../dir/file.txt (файл лежит в папке dir, которая расположена на один уровень выше от текущей)
# ../../file.txtp (файл лежит в папке, которая расположена на два уровня выше от текущей)
# with open('/home/ubuntu/workspace/python/tasks/6_files/ospf.txt', 'r') as f:
# with open('./ospf.txt', 'r') as f:
# with open('../6_files/ospf.txt', 'r') as f:

- открытие файла с обработкой исключения 
temp_list=[]    
                                              # открытие файла
try:                                          # обработка исключения на наличие файла
    with open('/home/ubuntu/workspace/python/tasks/6_files/CAM_table.txt', 'r') as f:
        for line in f:
           temp_list.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
except IOError:
    print('No such file')

print('\n'.join(temp_list)) 
---------------------------------------


with open('r1.txt', 'r') as f:
    for line in f:
        print(line)

# при выводе, между строками файла были лишние пустые строки, так как print добавляет ещё один перевод строки.
# чтобы избавиться от этого, можно использовать метод rstrip :

with open('r1.txt', 'r') as f:
    for line in f:
        print(line.rstrip())

# использование с другими конструкциями
with open('r1.txt', 'r') as f:
    print(f.read())

# определяем для открытого файла переменую f
# и выполняет набор инструкций. После их выполнения файл автоматически закрывается. 
# Даже если при выполнении инструкций в блоке with возникнут какие-либо исключения,
# то файл все равно закрывается.

with open(file_name, 'w') as f:        # определяем для открытого файла переменую f
    for	line in temp_list_three:
        f.write(line+'\n')             # +'\n' для переноса строк
        
# Открытие двух файлов
# записать некоторые строки из одного файла, в другой
with open('r1.txt') as src, open('result.txt', 'w') as dest:
    for	line in src:
        if line.startswith('service'):
            dest.write(line)

cat	result.txt

# service	timestamps	debug	datetime	msec	localtime	show-timezone	year
# service	timestamps	log	datetime	msec	localtime	show-timezone	year
# service	password-encryption
# service	sequence-numbers

# или


with open('r1.txt') as src:
    with open('result.txt',	'w') as dest:
        for line in src:
            if line.startswith('service'):
                dest.write(line)


"""открытие/закрытие
"""
file = open('file_name.txt', 'r')

# 'file_name.txt' - имя файла тут можно указывать не только имя, но и путь (абсолютный или относительный)
#  'r' - режим открытия файла
#        Режимы открытия файлов:  r - read; a - append; w - write
    r   #  - открыть файл только для чтения (значение по умолчанию)
    r+  #  - открыть файл для чтения и записи
    w   #  - открыть файл для записи
        #      если файл существует, то его содержимое удаляется
        #      если файл не существует, то создается новый
    w+  #  - открыть файл для чтения и записи
        #      если файл существует, то его содержимое удаляется
        #      если файл не существует, то создается новый
    a   #  - открыть файл для дополнения записи. Данные добавляются в конец файла
    a+  #  - открыть файл для чтения и записи. Данные добавляются в конец файла


"""чтение
"""
read()      # - считывает содержимое файла в строку
readline()  # - считывает файл построчно
readlines() # - считывает строки файла и создает список из строк

"""
            file - r1.txt:
!
service timestamps debug datetime msec localtime show-timezone year
service timestamps log datetime msec localtime show-timezone year
service password-encryption
service sequence-numbers
!
no ip domain lookup
!
ip ssh version 2
!
"""

f = open('r1.txt')
f.read()
# '!\nservice timestamps debug datetime msec localtime show-timezone year\nservi
# ce timestamps log datetime msec localtime show-timezone year\nservice password-encrypt
# ion\nservice sequence-numbers\n!\nno ip domain lookup\n!\nip ssh version 2\n!\n'

f.read()    #  повторном чтении файла отображается пустая строка. Так происходит
            # из-за того, что при вызове метода read() , считывается весь файл. И после того, как
            # файл был считан, курсор остается в конце файла. Управлять положением курсора
            # можно с помощью метода seek() . 
# ''

f = open('r1.txt')
f.readline()
# '!\n'
f.readline()
# 'service timestamps debug datetime msec localtime show-timezone

# аналогично

f = open('r1.txt')
for line in f:
    print(line)
    
    
    
f = open('r1.txt')
f.readlines()

# ['!\n',
# 'service timestamps debug datetime msec localtime show-timezone year\n',
# 'service timestamps log datetime msec localtime show-timezone year\n',
# 'service password-encryption\n',
# 'service sequence-numbers\n',
# '!\n',
# 'no ip domain lookup\n',
# '!\n',
# 'ip ssh version 2\n',
# '!\n']

f = open('r1.txt')
f.read().split('\n')   # убрать перевод строки
                       # Обратите внимание, что последний элемент списка - пустая строка.
                       # Если перед выполнением split() , воспользоваться методом rstrip() , список будет
                       # без пустой строки в конце:
f.read().rstrip().split('\n')

print(f.read())
f.seek(0)              # seek , курсор был переведен в начало файла, можно опять считывать содержимое:
print(f.read())

"""запись
"""

#   При записи, очень важно определиться с режимом открытия файла, чтобы случайно его не удалить:

write()      # - записать в файл одну строку (ожидает строку для записи)
writelines() # - позволяет передавать в качестве аргумента список строк (ожидает список строк для записи)

cfg_lines = ['!',    # список для записи
    'service timestamps debug datetime msec localtime show-timezone year',
    'service timestamps log datetime msec localtime show-timezone year',
    'ip ssh version 2',
    '!']

f = open('r2.txt', 'w')   # Открытие файла r2.txt в режиме для записи

cfg_lines_as_string = '\n'.join(cfg_lines)  # Преобразуем список команд в одну большую строку

f.write(cfg_lines_as_string)    # Запись строки в файл:

f.write('\nhostname r2')        # Аналогично можно добавить строку вручную:

f.close()                       # После завершения работы с файлом, его необходимо закрыть:
 
cat r2.txt                      # посмотреть содержимое файла:

#  writelines()
cfg_lines = ['!',
    'service timestamps debug datetime msec localtime show-timezone year',
    'service timestamps log datetime msec localtime show-timezone year',
    'service password-encryption',
    'ip ssh version 2',
    '!']
f = open('r2.txt', 'w')
f.writelines(cfg_lines)
f.close()   # нужен для того, чтобы содержимое файла было записано на диск.
cat r2.txt
# !service timestamps debug datetime msec localtime show-timezone yearservice timestamps
# log datetime msec localtime show-timezone yearservice password-encryptionservice sequ
# ence-numbers!no ip domain lookup!ip ssh version 2!


# В результате, все строки из списка, записались в одну строку файла, так как в конце строк не было символа \n .

# Добавить перевод строки

cfg_lines2 = []
for line in cfg_lines:
    cfg_lines2.append( line + '\n' )

# Или использовать list comprehensions:

cfg_lines3 = [ line + '\n' for line in cfg_lines ]

"""Закрытие файлов
"""
close()    

# Метод close встречался в разделе запись файлов.
# Там он был нужен для того, чтобы содержимое файла было записано на диск.

