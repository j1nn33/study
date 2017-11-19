#Из строк command1 и command2 получить список VLANов, которые есть и в команде
#command1 и в команде command2.
#результатом должен быть список: пересечение [1, 3, 100] Этот список содержит подсказку по типу итоговых данных.
#объединение ['20', '300', '1', '10', '30', '100', '200', '3']

command1 = 'switchport trunk allowed vlan 1,3,10,20,30,100'
command2 = 'switchport trunk allowed vlan 1,3,100,200,300'

list_command1 = command1.split(" ")  # преобразование строки в список по определенному разделителю " "
list_command2 = command2.split(" ") 

list_command1 = list_command1[4::]   # забираем конечный элемент списка
list_command2 = list_command2[4::]

command1 = ','.join(list_command1)   # преобразовываем список в строку с '' - разделитель между элементами списка соответственно
command2 = ','.join(list_command2)

list_command1 = command1.split(",")  # преобразование строки в список по определенному разделителю " "
list_command2 = command2.split(",") 

set_list1 = set(list_command1)
set_list2 = set(list_command2)
set_list = set_list1 & set_list2 
print (set_list)
# объединение 
list_command1.extend(list_command2)  # объединение двух списков
print (list_command1)
set_command = set(list_command1)     # преобразование к множеству 
print (list(set_command))

# пересечение
list_command = list(set_list)        # преобразование множества к списку
print (list_command)