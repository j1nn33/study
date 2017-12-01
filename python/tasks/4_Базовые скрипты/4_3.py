"""
Скрипт запрашиваeт у пользователя: 
    информацию о режиме интерфейса (access/trunk),
'Enter interface mode (access/trunk): '
    номере интерфейса (тип и номер, вида Gi0/3)
'Enter interface type and number: '
    номер VLANа (для режима trunk будет вводиться список VLANов)
'Enter vlan(s): '
В зависимости от выбранного режима, на стандартный поток вывода
возвращается соответствующая конфигурация access или trunk
(шаблоны команд находятся в списках access_template и trunk_template).
сначала идти строка interface и подставлен номер интерфейса, а
затем соответствующий шаблон, в который подставлен номер VLANа (или список VLANов).
"""
    # СПИСКИ и СЛОВАРИ
vlan=[]                                                          # создаем пустой список
vlan_t=0                                                         # инициализируем переменную vlan_t = 0 для access режима
access_template = ['switchport mode access',                     # списки с режимами
                   'switchport access vlan {}',
                   'switchport nonegotiate',
                   'spanning-tree portfast',
                   'spanning-tree bpduguard enable']
trunk_template = ['switchport trunk encapsulation dot1q',
                  'switchport mode trunk',
                  'switchport trunk allowed vlan {}']
net_mode= {'access':access_template, 'trunk':trunk_template}    # словарь исппользуется для выбора режима
vlan_list={'access':vlan_t, 'trunk':vlan}                       # словарь используется для выбора номера или списка vlan
    # ВВЕДЕНИЕ ДАННЫХ
int_mode=input('Enter interface mode (access/trunk):')
#int_mode = 'access'
#int_mode = 'trunk'
eth_type=input('Enter interface type and number: ')
#eth_type = 'Fa0/7'
vlan_t=int(input('Enter vlan(s): '))
#vlan_t=3
    # ОБРАБОТКА ДАННЫХ
vlan.append(vlan_t)         # заполнение списка vlan
vlan.append(4)
vlan.append(7)
#print(vlan)
    # ВЫВОД ДАННЫХ
print('interface {}'.format(eth_type))
print('\n'.join(net_mode[int_mode]).format(vlan_list[int_mode]))
# Сначала элементы списка net_mode (int_mode - элемент списка access/trunk ) объединяются в строку,
# которая разделена символом \n , 
# в строку подставляется (вместо {}  списки с режимами)
# список (vlan_list) элемент (int_mode) , используя форматирование строк.

"""
interface Fa0/6
switchport mode access
switchport access vlan 3
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard 

interface Fa0/7
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 2,3,4,5
"""

