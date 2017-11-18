
#"-------------СЛОВАРИ"
#"Данные в словаре хранятся в формате ключ – значение"
d1 = dict ( Ivan = "manager" , Mark = "worker" )
print (d1)

# {'Ivan': 'manager', 'Mark': 'worker'}

# "добавление элемента"
d1[ "China" ] = "Beijing"

# "Удаление элемента через ключ"
del d1[ " Ivan" ]

# В словаре в качестве значения можно использовать словарь:
london_co = {
    'r1' : {
    'hostname': 'london_r1',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': '10.255.0.1'
    },
    'r2' : {
    'hostname': 'london_r2',
    'location': '21 New Globe Walk',
    'vendor': 'Cisco',
    'model': '4451',
    'ios': '15.4',
    'ip': '10.255.0.2'
    }
}

london_co['r1']['ios']
# '15.4'
# Методы работы со словарем

clear() # очистить словарь
copy()  # создать полную копию словаря
get()   # запрашивает ключ и, если его нет, вместо ошибки возвращает None

keys(), values(), items()

london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}
london.keys()
# dict_keys(['name', 'location', 'vendor'])
london.values()
# dict_values(['London1', 'London Str', 'Cisco'])
london.items()
# dict_items([('name', 'London1'), ('location', 'London Str'), ('vendor', 'Cisco')])

del() # Удалить ключ и значение

london = {'name': 'London1', 'location': 'London Str', 'vendor': 'Cisco'}
del(london['name'])

update  # позволяет добавлять в словарь содержимое другого словаря
r1 = {'name': 'London1', 'location': 'London Str'}
r1.update({'vendor': 'Cisco', 'ios':'15.2'})
r1
# {'ios': '15.2', 'location': 'London Str', 'name': 'London1', 'vendor': 'Cisco'}

""" СОЗДАНИЕ СЛОВАРЯ"""
r1 = {'model': '4451', 'ios': '15.4'}
r2 = dict(model='4451', ios='15.4')
r3 = dict([('model','4451'), ('ios','15.4')])

# dict.fromkeys
# В ситуации, когда надо создать словарь с известными ключами, но, пока что, пустыми
# значениями (или одинаковыми значениями)
d_keys = ['hostname', 'location', 'vendor', 'model', 'ios', 'ip']
r1 = dict.fromkeys(d_keys)
r1
"""
{'ios': None,
 'ip': None,
 'hostname': None,
 'location': None,
 'model': None,
 'vendor': None}
"""

router_models = ['ISR2811', 'ISR2911', 'ISR2921', 'ASR9002']
models_count = dict.fromkeys(router_models, 0)
models_count
# {'ASR9002': 0, 'ISR2811': 0, 'ISR2911': 0, 'ISR2921': 0}

################################################################
################################################################
# Кортеж (Tuple)
# Кортеж - это неизменяемый упорядоченный тип данных.

list_keys = ['hostname', 'location', 'vendor', 'model', 'IOS', 'IP']
tuple_keys = tuple(list_keys)
tuple_keys
# ('hostname', 'location', 'vendor', 'model', 'IOS', 'IP')

################################################################
################################################################
# Множество (Set)
# Множество - это изменяемый неупорядоченный тип данныхкоторые разделены между
# собой запятой и заключены в фигурные скобки. В множестве всегда
# содержатся только уникальные элементы.

vlans = [10, 20, 30, 40, 100, 10]
set(vlans)
# {10, 20, 30, 40, 100}

# add

set.add(50)
set
# {10, 20, 30, 40, 50}

# discard()
# Метод discard() позволяет удалять элементы, не выдавая ошибку, если элемента в
# множестве нет:

# Объединение множеств можно получить с помощью метода union() или оператора |
vlans1 = {10,20,30,50,100}
vlans2 = {100,101,102,102,200}
vlans1.union(vlans2)
# {10, 20, 30, 50, 100, 101, 102, 200}
vlans1 | vlans2
#: {10, 20, 30, 50, 100, 101, 102, 200}

# Множество из строки:
set('long long long long string')
# {' ', 'g', 'i', 'l', 'n', 'o', 'r', 's', 't'}
# Множество из списка:
set([10,20,30,10,10,30])
# {10, 20, 30}
# Генератор множеств:
set2 = {i + 100 for i in range(10)}
set2
# {100, 101, 102, 103, 104, 105, 106, 107, 108, 109}