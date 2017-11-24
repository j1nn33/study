"""
Дополнить скрипт из задания 4.3 таким образом, чтобы, в зависимости от выбранного
режима, задавались разные вопросы в запросе о номере VLANа или списка VLANов:
для access: 'Enter VLAN number:'
для trunk: 'Enter allowed VLANs:'
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
vlan_question={'access':'Enter VLAN number: ', 'trunk':'Enter allowed VLANs: '}                       # словарь используется для выбора номера или списка vlan
    # ВВЕДЕНИЕ ДАННЫХ
#int_mode=input('Enter interface mode (access/trunk):')
#int_mode = 'access'
int_mode = 'trunk'
#eth_type=input('Enter interface type and number: ')
eth_type = 'Fa0/7'
print(vlan_question[int_mode])                                  # выводится вопрос в зависимости от режима
vlan_t=int(input())
vlan_t=3
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
