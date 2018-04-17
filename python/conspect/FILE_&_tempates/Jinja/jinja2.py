pip install jinja2

"""Идея Jinja очень проста: разделение данных и шаблона. Это позволяет использовать
   один и тот же шаблон, но подставлять в него разные данные.
   В самом простом случае шаблон - это просто текстовый файл, в котором указаны
   места подстановки значений с помощью переменных Jinja.



Пример шаблона Jinja:

{{name}} -  переменные записываются в двойных фигурных скобках.
            При выполнении скрипта эти переменные заменяются нужными значениями.

"""

hostname {{name}}
!
interface Loopback255
description Management loopback
ip address 10.255.{{id}}.1 255.255.255.255
!
interface GigabitEthernet0/0
description LAN to {{name}} sw1 {{int}}
ip address {{ip}} 255.255.255.0
!
router ospf 10
router-id 10.255.{{id}}.1
auto-cost reference-bandwidth 10000
network 10.0.0.0 0.255.255.255 area 0



"""
Этот шаблон может использоваться для генерации конфигурации разных устройств с
помощью подстановки других наборов переменных.
Пример скрипта с генерацией файла на основе шаблона Jinja (файл
basic_generator.py)"""


from jinja2 import Template                 # Jinja2 импортирует класс Template

template = Template('''                     # создается объект template, которому передается шаблон
hostname {{name}}
!
interface Loopback255
description Management loopback
ip address 10.255.{{id}}.1 255.255.255.255
!
interface GigabitEthernet0/0
description LAN to {{name}} sw1 {{int}}
ip address {{ip}} 255.255.255.0
!
router ospf 10
router-id 10.255.{{id}}.1
auto-cost reference-bandwidth 10000
network 10.0.0.0 0.255.255.255 area 0
''')

# в словаре liverpool ключи должны быть такими же, как имена переменных в шаблоне

liverpool = {'id':'11', 'name':'Liverpool', 'int':'Gi1/0/17', 'ip':'10.1.1.10'}  
print(template.render(liverpool))


'''
Examples:

$ python generator.py

hostname Liverpool
!
interface Loopback255
 description Management loopback
 ip address 10.255.11.1 255.255.255.255
!
interface GigabitEthernet0/0
 description LAN to Liverpool sw1 Gi1/0/17
 ip address 10.1.1.10 255.255.255.0
!
router ospf 10
 router-id 10.255.11.1
 auto-cost reference-bandwidth 10000
 network 10.0.0.0 0.255.255.255 area 0
'''

Пример использования Jinja2
В этом примере логика разнесена в 3 разных файла (все файлы находятся в каталоге example_1):
    router_template.py     - шаблон
    routers_info.yml       - в этом файле в виде списка словарей (в формате YAML)
                             находится информация о маршрутизаторах, для которых нужно сгенерировать
                             конфигурационный файл
router_config_generator.py - в этом скрипте импортируется файл с шаблоном и
                             считывается информация из файла в формате YAML, а затем генерируются
                             конфигурационные файлы маршрутизаторов
                             
Файл router_config_generator.py: импортирует шаблон template_r1 

из файла routers_info.yml список параметров считывается в переменную routers
Затем в цикле перебираются объекты (словари) в списке routers:

название файла, в который записывается итоговая конфигурация, состоит из поля
name в словаре и строки _r1.txt
например, Liverpool_r1.txt
файл с таким именем открывается в режиме для записи
в файл записывается результат рендеринга шаблона с использованием текущего словаря
конструкция with сама закрывает файл управление возвращается в начало цикла (пока не переберутся все словари)

Запускаем файл router_config_generator.py:
$ python router_config_generator.py
В результате получатся три конфигурационных файла:
Liverpool_r1.txt
Bristol_r1.txt
Coventry_r1.txt                             

----------------------------------------------------

router_config_generator.py


импортирует из модуля jinja2:
FileSystemLoader - загрузчик, который позволяет работать с файловой системой
тут указывается путь к каталогу, где находятся шаблоны
в данном случае шаблон находится в каталоге templates
Environment - класс для описания параметров окружения:
в данном случае указан только загрузчик
но в нем можно указывать методы обработки шаблона
Обратите внимание, что шаблон теперь находится в каталоге templates.

----------------------------------------------------

        Синтаксис шаблонов Jinja2
В шаблонах Jinja2 можно использовать:
    переменные
    условия (if/else)
    циклы (for)
    фильтры - специальные встроенные методы, которые позволяют делать
    преобразования переменных
    тесты - используются для проверки, соответствует ли переменная какому-то условию

Кроме того, Jinja поддерживает наследование между шаблонами, а также позволяет
добавлять содержимое одного шаблона в другой.

Для генерации шаблонов будет использоваться скрипт cfg_gen.py

нужно вызвать скрипт и передать ему два
аргумента:
    шаблон
    файл с переменными в формате YAML
 

$ python cfg_gen.py templates/variables.txt data_files/vars.yml

=================================================================

Контроль символов whitespace

Параметр trim_blocks удаляет первую пустую строку после блока конструкции, если
его значение равно True (по умолчанию False).

--------
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))

$ python cfg_gen.py templates/env_flags.txt data_files/router.yml
router bgp 100

neighbor 10.0.0.2 remote-as 100
neighbor 10.0.0.2 update-source lo100

neighbor 10.0.0.3 remote-as 100
neighbor 10.0.0.3 update-source lo100
-----------------------
env = Environment(loader = FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)

$ python cfg_gen.py templates/env_flags.txt data_files/router.yml
router bgp 100
neighbor 10.0.0.2 remote-as 100
neighbor 10.0.0.2 update-source lo100
neighbor 10.0.0.3 remote-as 100
neighbor 10.0.0.3 update-source lo100


--------------------------

Цикл for позволяет проходиться по элементам последовательности.
Цикл for должен находиться внутри символов {% %} . Кроме того, нужно явно
указывать завершение цикла:

{% for vlan in vlans %}
vlan {{ vlan }}
{% endfor %}

Пример шаблона templates/for.txt с использованием цикла:


hostname {{ name }}
interface Loopback0
ip address 10.0.0.{{ id }} 255.255.255.255
{% for vlan, name in vlans.items() %}
vlan {{ vlan }}
name {{ name }}
{% endfor %}

================================

if/elif/else
if позволяет добавлять условие в шаблон. Например, можно использовать if, чтобы
добавлять какие-то части шаблона в зависимости от наличия переменных в словаре с
данными.
Конструкция if также должна находиться внутри {% %} . Нужно явно указывать
окончание условия:

{% if ospf %}
router ospf 1
router-id 10.0.0.{{ id }}
auto-cost reference-bandwidth 10000
{% endif %}

Пример шаблона templates/if.txt:

hostname {{ name }}
interface Loopback0
ip address 10.0.0.{{ id }} 255.255.255.255
{% for vlan, name in vlans.items() %}
vlan {{ vlan }}
name {{ name }}
{% endfor %}

================================


Фильтры


В Jinja переменные можно изменять с помощью фильтров. Фильтры отделяются от
переменной вертикальной чертой (pipe | ) и могут содержать дополнительные
аргументы.


Кроме того, к переменной могут быть применены несколько фильтров. В таком случае
фильтры просто пишутся последовательно, и каждый из них отделен вертикальной
чертой.

default

Фильтр default позволяет указать для переменной значение по умолчанию. Если
переменная определена, будет выводиться переменная, если переменная не
определена, будет выводиться значение, которое указано в фильтре default.
Пример шаблона templates/filter_default.txt:

router ospf 1
auto-cost reference-bandwidth {{ ref_bw | default(10000) }}
{% for networks in ospf %}
network {{ networks.network }} area {{ networks.area }}
{% endfor %}

Если переменная ref_bw определена в словаре, будет подставлено её значение. Если
же переменной нет, будет подставлено значение 10000.


===========================================

        dictsort

Фильтр dictsort позволяет сортировать словарь. По умолчанию сортировка
выполняется по ключам. Но, изменив параметры фильтра, можно выполнять
сортировку по значениям.

Синтаксис фильтра:
dictsort(value, case_sensitive=False, by='key')

После того, как dictsort отсортировал словарь, он возвращает список кортежей, а не словарь.

Пример шаблона templates/filter_dictsort.txt с использованием фильтра dictsort:

{% for intf, params in trunks | dictsort %}
interface {{ intf }}
{% if params.action == 'add' %}
switchport trunk allowed vlan add {{ params.vlans }}
{% elif params.action == 'delete' %}
switchport trunk allowed vlan remove {{ params.vlans }}
{% else %}
switchport trunk allowed vlan {{ params.vlans }}
{% endif %}
{% endfor %}

Обратите внимание, что фильтр ожидает словарь, а не список кортежей или итератор


===============================================

        join

Фильтр join работает так же, как и метод join в Python.
С помощью фильтра join можно объединять элементы последовательности в строку с
опциональным разделителем между элементами.
Пример шаблона templates/filter_join.txt с использованием фильтра join:
{% for intf, params in trunks | dictsort %}
interface {{ intf }}
{% if params.action == 'add' %}
switchport trunk allowed vlan add {{ params.vlans | join(',') }}
{% elif params.action == 'delete' %}
switchport trunk allowed vlan remove {{ params.vlans | join(',') }}
{% else %}
switchport trunk allowed vlan {{ params.vlans | join(',') }}
{% endif %}
{% endfor %}

===============================================


set
Внутри шаблона можно присваивать значения переменным. Это могут быть новые
переменные, а могут быть измененные значения переменных, которые были переданы
шаблону.

{% for intf, params in trunks | dictsort %}
{% set vlans = params.vlans %}
{% set action = params.action %}

