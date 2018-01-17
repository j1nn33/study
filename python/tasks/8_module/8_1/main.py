#                       PART 1
#  импортировать нужные функции из файла my_func.
#                       PART 2
#  - Файл main.py должен ожидать как аргумент имя конфигурационного файла коммутатора.
#  - Имя конфигурационного файла передать как аргумент функции get_int_vlan_map
#      (из задания 7.3-7.3a)
#  - На выходе функции, мы должны получить кортеж двух словарей.
#                       PART 3
#  - Словари, соответственно, надо передать функциям:
#      generate_access_config (из задания 7.1-7.1a)
#      generate_trunk_config (из задания 7.2)
#                       PART 4
#  - Эти функции, в свою очередь, возвращают список со строками готовой
#     конфигурации которую надо записать в файл result.txt в виде стандартной
#     конфигурации (то есть, строк)

#####################################################

from my_func import *
#testing()

from sys import argv 

# запуск скрипта 
# $ python3 /home/ubuntu/workspace/python/tasks/8_module/8_1/main.py config_sw1.txt
# раскоментировать 2 строки и имя файла можно задавать при вводе в терминиле как по условию 
#file_name = argv[1] 
#file_name="/home/ubuntu/workspace/python/tasks/8_module/8_1/"+file_name 

# чтобы не задавить имя при запуске программы
file_name="/home/ubuntu/workspace/python/tasks/8_module/8_1/config_sw1.txt"
print('  PART 1  - COMPLETE ')
d_access, d_trunk = get_int_vlan_map(file_name)
print('  PART 2  - COMPLETE ')
#print ('cловарь портов в режиме access')
#print (d_access)                                        
#print ('словарь портов в режиме trunk')
#print (d_trunk)     
#########################################
list_access=[]
list_trunc=[]
list_total=[]

a = input('psecurity in default = False, input psecurity ( True/False ) ',)      # запрос на ввод параметра psecurity
if a=='True':                                                                    # вызов функции в зависимости от параметра
    list_access = generate_access_config(d_access, True)
else:
    list_access = generate_access_config(d_access)

print ('ACCESS_CONFIGURE_IN_MAIN_COMPLETE')
list_trunc = generate_trunk_config(d_trunk)
print ('TRUNK_CONFIGURATION_IN_MAINCOPLETE')
print('  PART 3  - COMPLETE ')
list_total = list_access+list_trunc
print('\n'.join(list_total))

file_name = "/home/ubuntu/workspace/python/tasks/8_module/8_1/result.txt"
try:                                        # обработка исключения на наличие файла
    with open(file_name, 'w') as f:
        for line in list_total:
            f.write(line+'\n')             # +'\n' для переноса строк
except IOError:
    print('ERROR IN WRITE PROCESS')



