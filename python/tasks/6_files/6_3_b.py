# Дополнить скрипт: 6.3a
# Запросить у пользователя ввод номера VLAN.
# Выводить информацию только по указанному VLAN.
temp_list_1=[]                                # инициализация вспомогательного списка  
                                              # открытие файла
try:                                          # обработка исключения на наличие файла
    with open('/home/ubuntu/workspace/python/tasks/6_files/CAM_table.txt', 'r') as f:
        for line in f:
           temp_list_1.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
except IOError:
    print('No such file')

"""обработка файла 
"""
                                              # удаление шапки
del temp_list_1 [0:6]
#print ('\n'.join(temp_list_1))

                                              # удаление третьей колонки
                                              # удаление элементов строки по номеру 

temp_list_2=[]  
for i in temp_list_1:
    i=(i.replace(i[24:36],''))                # замена элементов строки c 24 по 36 на ''
    temp_list_2.append(i)
    
#print ('исходный список')
print ('\n'.join(temp_list_2))

                                              # дополнение по условию задачи
vlan=input('Input vlan  ',)
print ('vlan',type(vlan),vlan)
j=0
for i in temp_list_2:
    if vlan == i[1:4]:
        print (i)
        j=j+1
    else:
        pass
if j==0:
    print ('vlan does not exist ')
