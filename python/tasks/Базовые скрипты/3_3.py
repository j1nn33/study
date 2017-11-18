# Получить из строки CONFIG список VLANов вида: ['1', '3', '10', '20', '30', '100']

CONFIG = 'switchport trunk allowed vlan 1,3,10,20,30,100'
print (CONFIG)

LIST_CONFIG =CONFIG.split(" ") # преобразование строки в список по определенному разделителю " "
print (LIST_CONFIG)
#       ['switchport', 'trunk', 'allowed', 'vlan', '1,3,10,20,30,100']

NEW_CONFIG = LIST_CONFIG [4::] # забираем конечный элемент списка
print (NEW_CONFIG)
#       ['1,3,10,20,30,100']

STRING = ','.join(NEW_CONFIG) # преобразовываем список в строку с '' - разделитель между элементами списка соответственно
print (STRING)
#       1,3,10,20,30,100

END_CONFIG =STRING.split(",") # преобразование строки в список по определенному разделителю ","
print (END_CONFIG)
#       ['1', '3', '10', '20', '30', '100']