# Переделать функциональность скрипта из задания 10.2a, в функцию generate_topology_from_cdp.
# Функция generate_topology_from_cdp должна быть создана с параметрами:
#       list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
#       save_to_file - этот параметр управляет тем, будет ли записан в файл topology.yaml, итоговый словарь
#                                                   значение по умолчанию - True
#      топология сохраняется только, если аргумент save_to_file указан равным True
# Функция возвращает словарь, который описывает топологию. Словарь должен быть в том же формате, что и в задании 10.2a.


# С помощью функции parse_sh_cdp_neighbors из задания 10.2, обработать вывод  команды sh cdp neighbor из файлов:
# Объединить все словари, которые возвращает функция parse_sh_cdp_neighbors, в
# один словарь topology и записать его содержимое в файл topology.yaml.
#  Структура словаря topology должна быть такой:
#            {'R4': {'Fa0/1': {'R5': 'Fa0/1'},
#                    'Fa0/2': {'R6': 'Fa0/0'}},
#             'R5': {'Fa0/1': {'R4': 'Fa0/1'}},
#             'R6': {'Fa0/0': {'R4': 'Fa0/2'}}}

import glob
import re
import os
import yaml
import draw_network_graph
# from draw_network_graph import draw_topology


#################################################################################################
# читает файлы и передает результат в виде списка
def read_file(file_name):
    temp_list = []
    try:  # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
                temp_list.append(
                    line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list


#################################################################################################
# парсим файл по строчно (получаем его как список строк)
def parse_sh_cdp_neighbors(out_file):
    dict_device = {}
    dict_temp = {}
    # цикл необходим тк в некоторых файлах сверх есть пустая строка
    # логика цикла ищем совпадение (служебный вывод либо None )
    # если служебный вывод то получаем из строки либо индекс строки либо индекс того чего ищем
    for line_in_file in out_file:
        posit = re.search('[>]', line_in_file)  # выражение для поиска >
        if posit:  # если совпадеине найдено
            posit = re.search('[>]', line_in_file).start()  # получаем позицию >
            my_name = line_in_file[:posit:]  # получаем имя устройсва до >

    for line_in_file in out_file:
        end_of_header_line = re.match('Device ID\s+', line_in_file)  # ищем нижню строчку шапки файла
        if end_of_header_line:  # если совпадеине найдено
            end_of_header_line = re.match('Device ID\s+', line_in_file).group()
            index_header = out_file.index(line_in_file)  # получаем индек этой строки в списк е out_file

    for line_in_file in out_file[index_header + 1::]:
        # R1           Eth 0/1         122           R S I           2811       Eth 0/0
        match = re.search('(?P<my_int>\S+)\s+(?P<neighbors_name>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',
                          line_in_file)

        #  'R5': {'Fa0/1': {'R4': 'Fa0/1'}}
        my_int = match.group('my_int')
        neighbors_name = match.group('neighbors_name')
        neighbors_int = match.group('neighbors_int')
        dict_temp2 = {}
        dict_temp1 = {}
        dict_temp1[my_int] = neighbors_int
        dict_temp2[neighbors_name] = dict_temp1
        dict_temp.update(dict_temp2)

    dict_device[my_name] = dict_temp
    # print (dict_device)
    return dict_device


#################################################################################################
# запись в yaml итоговой топологии (итогового словаря)
def generate_topology_from_cdp(full_name_list_of_file, save_to_file=True):
    print ('save_to_file ',save_to_file)
    #print ('\n'.join(full_name_list_of_file))
    list_of_file = []
    dict_total = {}
    print ('########################')
    for file_name in full_name_list_of_file:
        #print(file_name)
        list_of_file = read_file(file_name)
        parse_sh_cdp_neighbors(list_of_file)
        dict_total.update(parse_sh_cdp_neighbors(list_of_file))
    #print (dict_total)
    print('SAVE TO FILE  - topology.yaml')
    if save_to_file:
        directory = os.getcwd() + '/'  # /home/ubuntu/workspace/python/tasks/10_type_files/10_2/
        topology_yaml = directory + 'topology.yaml'
        print(topology_yaml)
        with open('sw_templates.yaml', 'w') as f:
            yaml.dump(dict_total, f)
        with open('sw_templates.yaml') as f:
            print( f.read())
        
    return dict_total


#################################################################################################
if __name__ == '__main__':
    directory = os.getcwd() + '/'  # /home/ubuntu/workspace/python/tasks/10_type_files/10_2/
    sh_cdp_n_files = glob.glob('sh_cd*')  # список имен файлов
    full_name_list_of_file = []
    list_in_file = []
    dict_total = {}

    for file_name in sh_cdp_n_files:
        full_name = directory + file_name
        full_name_list_of_file.append(full_name)
    print (full_name_list_of_file)
    # ваврианы вызова функции с параметром по умолчанию
    save_to_file = True
    # generate_topology_from_cdp (full_name_list_of_file)

    #save_to_file = False
    dict_total = generate_topology_from_cdp(full_name_list_of_file, save_to_file)


