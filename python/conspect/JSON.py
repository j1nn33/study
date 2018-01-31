JSON
"""Чтение"""
{
  "access": [
    "switchport mode access",
    "switchport access vlan",
    "switchport nonegotiate",
    "spanning-tree portfast",
    "spanning-tree bpduguard enable"
  ],
  "trunk": [
    "switchport trunk encapsulation dot1q",
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan"
  ]
}

# Для чтения в модуле json есть два метода:
json.load()  # - метод считывает файл в формате JSON и возвращает объекты Python
json.loads() # - метод считывает строку в формате JSON и возвращает объекты Python


# json.load()

import json

with open('sw_templates.json') as f:
    templates = json.load(f)
    for section, commands in templates.items():
        print(section)
        print('\n'.join(commands))
        
#{'access': ['switchport mode access', 'switchport access vlan', 'switchport nonegotiate',
# 'spanning-tree portfast', 'spanning-tree bpduguard enable'], 'trunk': ['switchport 
# trunk encapsulation dot1q', 'switchport mode trunk', 'switchport trunk native vlan 999',
# 'switchport trunk allowed vlan']}
"""
access
switchport mode access
switchport access vlan
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
trunk
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 999
switchport trunk allowed vlan
"""
# json.loads()
import json

with open('sw_templates.json') as f:
    file_content = f.read()
    templates = json.loads(file_content)
    print(templates)
    for section, commands in templates.items():
        print(section)
        print('\n'.join(commands))

# Результат будет аналогичен предыдущему выводу

"""Запись"""

json.dump()  - метод записывает объект Python в файл в формате JSON
json.dumps() - метод возвращает строку в формате JSON

# json.dumps()

import json
trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
                   
to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    f.write(json.dumps(to_json))

with open('sw_templates.json') as f:
    print(f.read())
    
# Метод json.dumps() подходит для ситуаций, когда надо вернуть строку в формате
# JSON. Например, чтобы передать ее API.

# json.dump()

import json

trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
                   
to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    json.dump(to_json, f)
with open('sw_templates.json') as f:
    print(f.read())
    
Дополнительные параметры методов записи

# Методам dump и dumps можно передавать дополнительные параметры для управления форматом вывода.
# По умолчанию эти методы записывают информацию в компактном представлении. 
# Как правило, когда данные используются другими программами, визуальное
# представление данных не важно. Если же данные в файле нужно будет считать
# человеку, такой формат не очень удобно воспринимать.
# модуль json позволяет управлять подобными вещами.
# Передав дополнительные параметры методу dump (или методу dumps)


import json
trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_json = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.json', 'w') as f:
    json.dump(to_json, f, sort_keys=True, indent=2)
with open('sw_templates.json') as f:
    print(f.read())
    
"""
{
 "access": [
   "switchport mode access",
   "switchport access vlan",
   "switchport nonegotiate",
   "spanning-tree portfast",
   "spanning-tree bpduguard enable"
 ],
 "trunk": [
   "switchport trunk encapsulation dot1q",
   "switchport mode trunk",
   "switchport trunk native vlan 999",
   "switchport trunk allowed vlan"
 ]
}

"""


Изменение типа данных

# Например, кортежи при записи в JSON превращаются в списки:
# JSON используются другие типы данных и не для всех типов данных Python есть соответствия.
Таблица конвертации данных Python в JSON:

Python          JSON
dict            object
list,tuple      array
str             string
int,float       number
True            true
False           false
None            null


Таблица конвертации JSON в данные Python:

JSON            Python
object          dict
array           list
string          str
number (int)    int
number (real)   float
true            True
false           False
null            None


Ограничение по типам данных
# В формат JSON нельзя записать словарь, у которого ключи - кортежи:
to_json = { ('trunk', 'cisco'): trunk_template, 'access': access_template}
with open('sw_templates.json', 'w') as f:
    json.dump(to_json, f)

#TypeError: key ('trunk', 'cisco') is not a string


# Но с помощью дополнительного параметра можно игнорировать подобные ключи:

to_json = { ('trunk', 'cisco'): trunk_template, 'access': access_template}
with open('sw_templates.json', 'w') as f:
    json.dump(to_json, f, skipkeys=True)
   
cat sw_templates.json
{"access": ["switchport mode access", "switchport access vlan", "switchport nonegotiate",
            "spanning-tree portfast", "spanning-tree bpduguard enable"]}

# Кроме того, в JSON ключами словаря могут быть только строки. Но, если в словаре
# Python использовались числа, ошибки не будет. Вместо этого выполнится конвертация
# чисел в строки:
    
d = {1:100, 2:200}
json.dumps(d)
#  '{"1": 100, "2": 200}'

