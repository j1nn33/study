# Создать функцию parse_sh_cdp_neighbors, которая обрабатывает вывод команды show cdp neighbors.
# Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла)
#            R4>show cdp neighbors
#            Device ID Local Intrfce Holdtme Capability Platform Port ID
#            R5 Fa 0/1 122 R S I 2811 Fa 0/1
#            R6 Fa 0/2 143 R S I 2811 Fa 0/0
# Функция должна возвращать словарь, который описывает соединения между устройствами.
#            {'R4': {'Fa0/1': {'R5': 'Fa0/1'},
#                    'Fa0/2': {'R6': 'Fa0/0'}}}

import glob
import re


#################################################################################################
# читает файлы и передает результат в виде списка 
def read_file (file_name):
    temp_list=[]    
    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list
#################################################################################################
# преобразует список строк в строку
def prepare_source_data (out_file):
    out_file_string = ''.join(out_file)
    #print (type(out_file_string))
    return out_file_string
#################################################################################################
def parse_line_head (out_file_string,reg):
    posit = re.search (reg,out_file_string).end()
    out_file_string = out_file_string[posit::]
    return out_file_string
#################################################################################################
def parse_line (out_file_string):
    """
    формируем промежуточный словарь вида {'Fa0/1': {'R5': 'Fa0/1'}
    """
    dict_temp = {}  
    while len(out_file_string):
        match =re.search('(?P<my_int>\S+)\s+(?P<neighbors_name>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',out_file_string) 
        # получение последнего знаячения этой строки
        posit_end=re.search('(?P<my_int>\S+)\s+(?P<neighbors_name>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',out_file_string).end()
        my_int = match.group('my_int')
        neighbors_name =match.group('neighbors_name')
        neighbors_int =match.group('neighbors_int') 
        dict_temp2= {}
        dict_temp1= {}
        dict_temp1[my_int]= neighbors_int  
        dict_temp2[neighbors_name]=dict_temp1
        #print (dict_temp2)
        out_file_string = out_file_string[posit_end::]           # срезаем общую строку на строку конфига из файла
        dict_temp.update(dict_temp2)
    #print (dict_temp)
    return dict_temp



#################################################################################################
def parse_sh_cdp_neighbors (out_file_string):
    dict_device = {}
    regex1 = '[>]'                       # выражение для поиска > 
    regex2 = 'ID'                        # 
    posit = re.search(regex1, out_file_string).start()   # поиск позиции > 
    my_name = out_file_string[:posit:]   # имя основного устройсва
    # удаление из строки служебной информации
    out_file_string = parse_line_head(out_file_string, regex2)
    out_file_string = parse_line_head(out_file_string, regex2)
   
    dict_device[my_name]= parse_line (out_file_string)
    return dict_device

#################################################################################################
if __name__ == '__main__':
    file_name = '/home/ubuntu/workspace/python/tasks/10_type_files/10_2/sh_cdp_n_sw1.txt'
    out_file = read_file (file_name)
    out_file_string = prepare_source_data (out_file)
    print (parse_sh_cdp_neighbors (out_file_string)) 