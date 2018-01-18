# Для выполнения этого задания, должен быть установлен graphviz:
# apt-get install graphviz
# И модуль python для работы с graphviz:
# pip install graphviz
# С помощью функции parse_cdp_neighbors из задания 8.2 и функции draw_topology из
# файла draw_network_graph.py, сгенерировать топологию, которая соответствует
# выводу команды sh cdp neighbor в файле sw1_sh_cdp_neighbors.txt
# В итоге, должен быть сгенерировано изображение топологии. topology.svg

import draw_network_graph
from draw_network_graph import draw_topology

def read_file(file_name):  # открытие файла
    temp_list = []
    try:  # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
                temp_list.append(
                    line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list


def convert_info(info):
    temp_str = str(info)
    return temp_str


def parse_cdp_neighbors(str_info):
    temp_in_func_info = {}
    print('IN FUNCTION')
    print()
    # print ()
    str_info = str_info[1:-1:]  # отрезаем начальные и конечные символы строки
    # print ('str_info ', type(str_info))
    temp_in_func_info = str_info.split(",")  # перегоняем строку в список
    # print ('temp_in_func_info',type(temp_in_func_info),temp_in_func_info)
    del temp_in_func_info[0:12:]  # срезаем лишние элементы
    # print (temp_in_func_info)
    out_dic = {}

    for elem_list in temp_in_func_info:
        # 'R1           Eth 0/1         122           R S I           2811       Eth 0/0'
        a = 'R4'
        b = elem_list[2:4:]
        c = elem_list[15:22:]
        d = elem_list[72:79:]
        key = []
        val = []
        key.append(a)  # заполнение ключа в виде списка
        key.append(c)
        key = tuple(key)
        print(key)
        val.append(b)  # заполнение значения в виде списка
        val.append(d)
        val = tuple(val)
        print(val)
        out_dic[key] = val
    """
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
    """
    print()
    print('RETURN TO THE MAIN PROGRAMM')
    return out_dic


################### MAIN ####################
total_dic = {}
# print ('temp_info ',type(temp_info),temp_info)
info = (read_file('/home/const/PycharmProjects/8_task_1/sw1_sh_cdp_neighbors.txt'))
print('READING FILE IS COMPLETE')
# print ('info')
# print ('\n'.join(info))
# print ()
str_info = convert_info(info)
# print ('str_info',type(str_info))
# print ()
# print (str_info)
print()
print('CONVERT INFO IS COMPLETE')
print()
total_dic = parse_cdp_neighbors(str_info)
print()
print('parse_cdp_neighbors is COMLETE')
print()
print(total_dic)
print ('DRAWING TOPOLOGY')
draw_network_graph.draw_topology(total_dic)     

