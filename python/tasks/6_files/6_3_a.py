# Сделать копию скрипта задания 6_3
# Дополнить скрипт:
# Отсортировать вывод по номеру VLAN

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


temp_list_2 = sorted(temp_list_2) 
print ('lllllllllllllllllllllll')
print ('\n'.join(temp_list_2))
# сортировка по номеру VLAN  
