#  Функции
# параметры фунции это аргументы которые она может принимать
# Параметры - это переменные, которые используются при создании функции.
# Аргументы - это фактические значения (данные), которые передаются функции при вызове
 
def fctname (a,b,c): # fctname - имя_функции (a,b,c) -параметры которые принимет функция
    """документация"""
    pass
    pass
    return res  # результат вызова, если нет возврата значения, то по умолчанию ввернется None
# вызов функции
x = fctname(1,2,3)
# x       - получить результат если он нужен
# fctname - имя функции
# (1,2,3) - один аргумент каждому параметру

def open_file( filename ):
    """Documentation string"""
    with open(filename) as f:
        print(f.read())         # вывод файла на стандартный поток
        return f.read()         # Для того, чтобы функция возвращала значение, которое потом можно, например,
                                # присвоить переменной, используется оператор return
                                # выражения, которые идут после return, не выполняются
  

open_file('r1.txt')             # вызов функции
# или
result = open_file('r1.txt')    
open_file.__doc__               # вызвать строку документации
'Documentation string'


     #  Пространства имен. Области видимости правило LEGB
"""
L (local)     - в локальной (внутри функции)
E (enclosing) - в локальной области объемлющих функций (это те функции, внутри которых находится наша функция)
G (global)    - в глобальной (в скрипте)
B (built-in)  - в встроенной (зарезервированные значения Python)
"""
"""    локальные переменные:
переменные, которые определены внутри функции
эти переменные становятся недоступными после выхода из функции
    глобальные переменные
переменные, которые определены вне функцииэти переменные 
'глобальны' только в пределах модуля например, чтобы они
были доступны в другом модуле, их надо импортировать
Пример локальной и глобальной переменной result:
"""
result = 'test string'        # глобальная переменная
def open_file( filename ):
    with open(filename) as f:
    result = f.read()         # локальная переменная
    return result
    
open_file('r1.txt')           # вывод локальной переменой result
'!\nservice timestamps debug datetime msec localtime show-timezone year\nservi
ce timestamps log datetime msec localtime show-timezone year\nservice password-encrypt
ion\nservice sequence-numbers\n!\nno ip domain lookup\n!\nip ssh version 2\n!\n'

result                        # вывод глобальной переменной result

'test string'

        # Параметры и аргументы функций
# ПАРАМЕТРЫЖ:
# - обязательными (но передать ровно столько, сколько указано параметров функции)
# - необязательными (опциональными, параметрами со значением по умолчанию)

def cfg_to_list(cfg_file, delete_exclamation): # c обязательными
# def cfg_to_list2(cfg_file, delete_exclamation=True): # c необязательными (параметры со значением по умолчанию)
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if delete_exclamation and line.startswith('!'):
                pass
            else:
                result.append(line.rstrip())
    return result
                                        # вызов функции   
cfg_to_list('r1.txt', True)             # с обязательными
print(cfg_to_list('r1.txt', False))     # с обязательными 

print(cfg_to_list2('r1.txt'))           # с необязательными 
print(cfg_to_list2('r1.txt', False))    # с необязательными
   
        # Типы аргументов функции (позиционные и ключевые)
# при вызове функции аргументы можно передавать двумя способами:
#  - позиционные - передаются в том же порядке, в котором они определены при создании функции. 
#    То есть, порядок передачи аргументов определяет, какое значение получит каждый
#  - ключевые - передаются с указанием имени аргумента и его значения.
# Позиционные и ключевые аргументы могут быть смешаны при вызове функции

cfg_to_list(delete_exclamation=False, cfg_file='r1.txt')  # ключевые параметры
cfg_to_list('r1.txt', delete_exclamation=True)            # смешаный

#      аргументы переменной длины
#   араметр, который принимает позиционные аргументы переменной длины, создается
# добавлением перед именем параметра звездочки. Имя параметра может быть любым,
# но, по договоренности, чаще всего, используют имя *args

def sum_arg(a, *args):
# def sum_arg(*args):       тоже вариант
    print(a, args)
    return a + sum(args)

#  Функция sum_arg создана с двумя параметрами:
#       параметр a
#       если передается как позиционный аргумент, должен идти первым
#       если передается как ключевой аргумент, то порядок не важен
#       параметр *args - ожидает аргументы переменной длины
#       сюда попадут все остальные аргументы в виде кортежа, эти аргументы могут отсутствовать



def sum_arg(a,**kwargs):
    print(a, kwargs)
    return a + sum(kwargs.values())

#  Ключевые аргументы переменной длины
# Параметр, который принимает ключевые аргументы переменной длины, создается
# добавлением перед именем параметра двух звездочек. Имя параметра может быть
# любым, но, по договоренности, чаще всего, используют имя **kwargs (от keyword arguments).

# Функция sum_arg создана с двумя параметрами:
#    параметр a
# если передается как позиционный аргумент, должен идти первым
# если передается как ключевой аргумент, то порядок не важен
#    Аргументы переменной длины
# параметр **kwargs - ожидает ключевые аргументы переменной длины
# сюда попадут все остальные ключевые аргументы в виде словаря
# эти аргументы могут отсутствовать

sum_arg(a=10,b=10,c=20,d=30)
sum_arg(b=10,c=20,d=30,a=10)
sum_arg(10,b=10,c=20,d=30)
# error
sum_arg(b=10,c=20,d=30,10)    # a можно указывать как позиционный аргумент, нельзя
                              # указывать позиционный аргумент после ключевого:


#       Распаковка аргументов *args и **kwargs позволяют выполнять ещё одну задачу - распаковку аргументов
# при передачи аргументов программно (до этого передавали их вручную), аргументы идут в виде объекта 

"""
Функция config_interface ожидает как аргумент: 
        intf_name   - имя интерфейса
        ip_address  - IP-адрес
        cidr_mask   - маску в формате CIDR (допускается и формат /24, и просто 24)
На выходе она выдает список строк для настройки интерфейса.

config_interface('Fa0/1', '10.0.1.1', '/25')
['interface Fa0/1', 'no shutdown', 'ip address 10.0.1.1 255.255.255.128']
"""
def config_interface(intf_name, ip_address, cidr_mask):
    interface = 'interface {}'
    no_shut = 'no shutdown'
    ip_addr = 'ip address {} {}'
    result = []
    result.append(interface.format(intf_name))
    result.append(no_shut)

    mask_bits = int(cidr_mask.split('/')[-1])                           # отсечение /
    bin_mask = '1'*mask_bits + '0'*(32-mask_bits)                       # bin_mask <class 'str'> 11111111111111111111111100000000
    dec_mask = [str(int(bin_mask[i:i+8], 2)) for i in range(0,25,8)]    # ['255', '255', '255', '0'] 
    dec_mask_str = '.'.join(dec_mask)                                   # 255.255.255.0

    result.append(ip_addr.format(ip_address, dec_mask_str))
    return result

"""    
нужно вызвать функцию и передать ей информацию, которая была получена из другого источника, к примеру, из БД.
Например, список interfaces_info, в котором находятся параметры для настройки интерфейсов:
"""
interfaces_info = [['Fa0/1', '10.0.1.1', '/24'],
                   ['Fa0/2', '10.0.2.1', '/24'],
                   ['Fa0/3', '10.0.3.1', '/24'],
                   ['Fa0/4', '10.0.4.1', '/24'],
                   ['Lo0', '10.0.0.1', '/32']]

# Если пройтись по списку в цикле и передавать вложенный список как аргумент
# функции, возникнет ошибка: тк функция ожидает три аргумента, а ей передан 1 аргумент - список.
# НЕ ПРАВИЛЬНО
#for info in interfaces_info:
#    print(config_interface(info))

# ПРАВИЛЬНО
for i in interfaces_info:
    print(config_interface(*i))
    
# Python сам 'распакует' список info и передаст в функцию элементы списка как аргументы

# Распаковка ключевых аргументов
# распаковка словаря чтобы передать его как ключевые аргументы.

"""Функция берет файл с конфигурацией, убирает часть строк и возвращает остальные
строки как список.
"""
def config_to_list(cfg_file, delete_excl=True,
                   delete_empty=True, strip_end=True):
    result = []
    with open(cfg_file) as f:
        for line in f:
            if strip_end:
                line = line.rstrip()                    # удаление '/n' знака переноса строки
            if delete_empty and not line:               # удаление пустых строк
                pass
            elif delete_excl and line.startswith('!'):  # удаление '!'
                pass
            else:
                result.append(line)
    return result

config_to_list('r1.txt')        # вызов функции

# cfg - список словарей 
cfg = [dict(cfg_file='r1.txt', delete_excl=True, delete_empty=True, strip_end=True),
       dict(cfg_file='r2.txt', delete_excl=False, delete_empty=True, strip_end=True),
       dict(cfg_file='r3.txt', delete_excl=True, delete_empty=False, strip_end=True),
       dict(cfg_file='r4.txt', delete_excl=True, delete_empty=True, strip_end=False)]
       
# ERROR
#for d in cfg:
#    print(config_to_list(d))
# Ошибка такая, так как все параметры, кроме имени файла, опциональны. И на стадии
# открытия файла возникает ошибка, так как вместо файла передан словарь.
# Если добавить ** перед передачей словаря функции, функция нормально отработает:

for d in cfg:
    print(config_to_list(**d))
    
# Python распаковывает словарь и передает его в функцию как ключевые аргументы.

# Пример использования ключевых аргументов
# переменной длины и распаковки аргументов

# Функция config_to_list 
# По умолчанию из конфигурации убираются пустые строки, перевод строки в конце
# строк и строки, которые начинаются на знак восклицания.

config_to_list('r1.txt')                              # По умолчанию 
config_to_list('r1.txt', delete_empty=False)          # пустые строки появились в списке

# Сделаем 'оберточную' функцию clear_cfg_and_write_to_file, которая берет файл
# конфигурации с помощью функции config_to_list, удаляет лишние строки и затем
# записывает строки в указанный файл.
# Но, при этом, мы не хотим терять возможность управлять тем, какие строки будут
# отброшены. То есть, необходимо, чтобы функция clear_cfg_and_write_to_file
# поддерживала те же параметры, что и функция config_to_list.

# 1 - var
# просто продублировать все параметры функции и передать их в функцию config_to_list:

def clear_cfg_and_write_to_file(cfg, to_file, delete_excl=True,
                                delete_empty=True, strip_end=True):
                                    
    cfg_as_list = config_to_list(cfg, delete_excl=delete_excl,
                    delete_empty=delete_empty, strip_end=strip_end)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))

# 2 -var   
# В функции clear_cfg_and_write_to_file явно прописаны её аргументы, а всё остальное
# попадет в переменную kwargs . Затем переменная kwargs передается как аргумент в
# функцию config_to_list. Но, так как переменная kwargs - это словарь, её надо
# распаковать при передаче функции config_to_list.

def clear_cfg_and_write_to_file(cfg, to_file, **kwargs):
    cfg_as_list = config_to_list(cfg, **kwargs)
    with open(to_file, 'w') as f:
        f.write('\n'.join(cfg_as_list))

"""
В этом примере **kwargs используется и для того, чтобы указать, что функция
clear_cfg_and_write_to_file может принимать аргументы переменной длины, и для
того, чтобы 'распаковать' словарь kwargs, когда мы передаем его в функцию
config_to_list.
"""
