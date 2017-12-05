# Переделать скрипт из задания 6.2b:
# передавать как аргументы скрипту:
# имя исходного файла конфигурации
# имя итогового файла конфигурации
# Внутри, скрипт должен отфильтровать те строки, в исходном файле конфигурации, в
# которых содержатся слова из списка ignore. И затем записать оставшиеся строки в
# итоговый файл.
# Проверить работу скрипта на примере файла config_sw1.txt.
ignore = ['duplex', 'alias', 'Current configuration']

#      ПЕРЕДАЧА АРГУМЕНТОВ СКРИПТУ (argv)
#     обработка файла при этом имя файла передается в качестве параметра
# python3 /home/ubuntu/workspace/python/tasks/6_files/6_2_a.py config_sw1.txt
from sys import argv                        # использование argv для работы с аргументами из модуля sys
file_name = argv[1]                         # argv[1] - Это срез списка. (cм ниже )  
                                            # $ python config_sw1.txt   
                                            # argv - это список все аргументы находятся в списке в виде строк
                                            # argv содержит не только аргументы, которые передали скрипту, но и название самого скрипта
                                            # Сначала идет имя самого скрипта, затем аргументы, в том же порядке.
file_name_out = argv[2]     
file_name="/home/ubuntu/workspace/python/tasks/6_files/"+file_name   # задание пути файла

temp_list_two=[]                                # инициализация вспомогательного списка  
                                            # открытие файла
try:                                        # обработка исключения на наличие файла
    with open(file_name, 'r') as f:
    #with open('/home/ubuntu/workspace/python/tasks/6_files/config_sw1.txt', 'r') as f:
        for line in f:
           #print(line)
           temp_list_two.append(line.rstrip())            # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
except IOError:
    print('No such file')

"""обработка файла 
"""
# проверка на список игнорируемых слов    
# ignore = ['duplex', 'alias', 'Current configuration']
temp_list_three=[' ']                  # пустой символ нужен для пустой строки в начале итогового списка
for x in temp_list_two[1::]:           # избавляемся от пустой строки в начале файла 
    j=0                                # используется для подсчета количества элементов в списке ignore
    for i in ignore:
        if x.find(i) !=-1:             # поиск игнорируемого слова i  в строке x 
            pass
        elif x.find(i) ==-1:           # если в списке нет игнорируемого слова о счетчик увеличивается на 1        
            j=j+1
            if j==len(ignore):         # строка заносится в финальный список после если проверилась по всем словам из списка ignore
                temp_list_three.append(x)
            else:
                pass
        else:
            pass

"""    вывод обработанной информаци
"""
#print('\n'.join(temp_list_three))      # на экран
                                       # имя выходного файла config_sw1_cleared.txt
                                      
file_name="/home/ubuntu/workspace/python/tasks/6_files/"+file_name_out   # задание пути файла
#file_name="/home/ubuntu/workspace/python/tasks/6_files/config_sw1_cleared.txt" 

# определяем для открытого файла переменую f
# и выполняет набор инструкций. После их выполнения файл автоматически закрывается. 
# Даже если при выполнении инструкций в блоке with возникнут какие-либо исключения,
# то файл все равно закрывается.

with open(file_name, 'w') as f:        # определяем для открытого файла переменую f
    for	line in temp_list_three:
        f.write(line+'\n')             # +'\n' для переноса строк
