"""
работа с конфигурационными файлами
использования enumerate для EEM
"""
"""работа с конфигурационными файлами
"""
    - открытие файла с обработкой исключения 
    - открытие файла
    - удаление (или пропуск) строк, которые начинаются на знак восклицания (для Cisco)
    - удаление (или пропуск) пустых строк
    - удаление символов перевода строки в конце строк
    - преобразование полученного результата в список
    
    
    
""" РЕАЛИЗАЦИЯ """
    - открытие файла с обработкой исключения 
temp_list=[]                                # открытие файла
try:                                          # обработка исключения на наличие файла
    with open('/home/ubuntu/workspace/python/tasks/6_files/CAM_table.txt', 'r') as f:
        for line in f:
           temp_list.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
except IOError:
    print('No such file')
print('\n'.join(temp_list)) 



    - удаление (или пропуск) строк, которые начинаются на знак восклицания (для Cisco)

def delete_exclamation_from_cfg(in_cfg, out_cfg):
    with open(in_cfg) as in_file:
        result = in_file.readlines()
    with open(out_cfg, 'w') as out_file:
        for line in result:
            if not line.startswith('!'):
                out_file.write(line)
                

delete_exclamation_from_cfg('input.txt', 'result.txt')

"""получает файл проверяет надо ли удалять ! 
   в строке справа удаляются символы перевода строки, и
   строка добавляется в словарь result.
"""

def cfg_to_list(cfg_file, delete_exclamation):
    result = []
    with open( cfg_file ) as f:
        for line in f:
            if delete_exclamation and line.startswith('!'):
                pass
            else:
                result.append(line.rstrip())
    return result
    
cfg_to_list('r1.txt', True)



"""использования enumerate для EEM
"""

#Выглядит applet EEM так:
event manager applet Fa0/1_no_shut
event syslog pattern "Line protocol on Interface FastEthernet0/0, changed state to down"
action 1 cli command "enable"
action 2 cli command "conf t"
action 3 cli command "interface fa0/1"
action 4 cli command "no sh"


# генерировать команды EEM на основании существующего списка команд (файл enumerate_eem.py)
# команды считываются из файла, а затем к каждой строке добавляется приставка, которая нужна для EEM.
import sys
config = sys.argv[1]
with open(config, 'r') as f:
    for i, command in enumerate(f, 1):
        print('action {:04} cli command "{}"'.format(i, command.rstrip()))
   
"""r1_config.txt

en
conf t
no int Gi0/0/0.300
no int Gi0/0/0.301
no int Gi0/0/0.302
int range gi0/0/0-2
channel-group 1 mode active
interface Port-channel1.300
encapsulation dot1Q 300
vrf forwarding Management
ip address 10.16.19.35 255.255.255.248
"""

$ python enumerate_eem.py r1_config.txt
action 0001 cli command "en"
action 0002 cli command "conf t"
action 0003 cli command "no int Gi0/0/0.300"
action 0004 cli command "no int Gi0/0/0.301"
action 0005 cli command "no int Gi0/0/0.302"
action 0006 cli command "int range gi0/0/0-2"
action 0007 cli command " channel-group 1 mode active"
action 0008 cli command "interface Port-channel1.300"
action 0009 cli command " encapsulation dot1Q 300"
action 0010 cli command " vrf forwarding Management"
action 0011 cli command " ip address 10.16.19.35 255.255.255.248"
