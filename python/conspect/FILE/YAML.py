YAML

"""Список"""

# Список может быть записан в одну строку:
[switchport mode access, switchport access vlan, switchport nonegotiate, 
 spanning-tree portfast, spanning-tree bpduguard enable]

# Или каждый элемент списка в своей строке:

- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable

# Когда список записан таким блоком, каждая строка должна начинаться
# с - (минуса и пробела), и все строки в списке должны быть на одном уровне отступа.

"""Словарь"""

# Словарь также может быть записан в одну строку:

{ vlan: 100, name: IT }

# Или блоком:

vlan: 100
name: IT

"""Строки"""

# Строки в YAML не обязательно брать в кавычки. Это удобно, но иногда всё же следует
# использовать кавычки. Например, когда в строке используется какой-то специальный
# символ (специальный для YAML).
# Такую строку, например, нужно взять в кавычки, чтобы она была корректно воспринята YAML:

command: "sh interface | include Queueing strategy:"

"""Комбинация элементов"""

# Словарь, в котором есть два ключа: access и trunk. Значения, которые соответствуют
# этим ключам - списки команд:
access:
- switchport mode access
- switchport access vlan
- switchport nonegotiate
- spanning-tree portfast
- spanning-tree bpduguard enable

trunk:
- switchport trunk encapsulation dot1q
- switchport mode trunk
- switchport trunk native vlan 999
- switchport trunk allowed vlan


# Список словарей:
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
  
Модуль PyYAML
# Для работы с YAML в Python используется модуль PyYAML. Он не входит в
# стандартную библиотеку модулей, поэтому его нужно установить:

pip install pyyaml

"""Чтение из YAML"""

# Файл info.yaml:
"""
- BS: 1550
  IT: 791
  id: 11
  name: Liverpool
  to_id: 1
  to_name: LONDON
- BS: 1510
  IT: 793
  id: 12
  name: Bristol
  to_id: 1
  to_name: LONDON
- BS: 1650
  IT: 892
  id: 14
  name: Coventry
  to_id: 2
  to_name: Manchester
"""

# Чтение из YAML (файл yaml_read.py):
import yaml
import pprint

with open('info.yaml') as f:
    templates = yaml.load(f)
    
pprint.pprint(templates)

"""
[{'BS': 1550,
  'IT': 791,
  'id': 11,
  'name': 'Liverpool',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1510,
  'IT': 793,
  'id': 12,
  'name': 'Bristol',
  'to_id': 1,
  'to_name': 'LONDON'},
 {'BS': 1650,
  'IT': 892,
  'id': 14,
  'name': 'Coventry',
  'to_id': 2,
  'to_name': 'Manchester'}]
"""


"""Запись в YAML"""

import yaml
trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk native vlan 999',
                  'switchport trunk allowed vlan']
access_template = ['switchport mode access',
                   'switchport access vlan',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    yaml.dump(to_yaml, f)
with open('sw_templates.yaml') as f:
    print f.read()
    
# Файл sw_templates.yaml выглядит таким образом:

# access: [switchport mode access, switchport access vlan, switchport nonegotiate, spanning-tree
# portfast, spanning-tree bpduguard enable]
# trunk: [switchport trunk encapsulation dot1q, switchport mode trunk, switchport trunk
# native vlan 999, switchport trunk allowed vlan]

# По умолчанию список записался в одну строку. Это можно изменить
#  надо добавить параметр  default_flow_style=False 
import yaml

to_yaml = {'trunk':trunk_template, 'access':access_template}

with open('sw_templates.yaml', 'w') as f:
    yaml.dump(to_yaml, f, default_flow_style=False)
with open('sw_templates.yaml') as f:
    print f.read()

# Теперь содержимое файла sw_templates.yaml выглядит таким образом:
# access:
# - switchport mode access
# - switchport access vlan
# - switchport nonegotiate
# - spanning-tree portfast
# - spanning-tree bpduguard enable
# trunk:
# - switchport trunk encapsulation dot1q
# - switchport mode trunk
# - switchport trunk native vlan 999
# - switchport trunk allowed vlan