# Для выполнения этого задания, должен быть установлен graphviz:
# apt-get install graphviz
# И модуль python для работы с graphviz:
# pip install graphviz
# С помощью функции parse_cdp_neighbors из задания 8.2 и функции draw_topology из
# файла draw_network_graph.py, сгенерировать топологию, которая соответствует
# выводу команды sh cdp neighbor в файле sw1_sh_cdp_neighbors.txt
# В итоге, должен быть сгенерировано изображение топологии. topology.svg

# import draw_network_graph
# from draw_network_graph import draw_topology

def read_file(file_name):                               # открытие файла
    temp_list = []
    try:                                                # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
                temp_list.append(
                    line.rstrip())                      # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('---FUNCTION---No such file')
    return temp_list


def convert_info(info):
    temp_str = str(info)
    return temp_str


def parse_cdp_neighbors_r(str_info,name):
    temp_in_func_info = {}
    #print('IN FUNCTION_R')
    #print()
    # print ()
    str_info = str_info[2:-1]                          # отрезаем начальные и конечные символы строки
    # print ('str_info ', type(str_info))
    temp_in_func_info = str_info.split(",")             # перегоняем строку в список
    #print ('temp_in_func_info',type(temp_in_func_info),temp_in_func_info)
    del temp_in_func_info[0:10:]                        # срезаем лишние элементы
    #print (temp_in_func_info)
    out_dic = {}

    for elem_list in temp_in_func_info:
        # " 'SW1              Eth 0/0           140          S I      WS-C3750-  Eth 0/1'"
        a = name
        print ('NAME',a)
        b = elem_list[2:8:]
        c = elem_list[19:26:]
        x = len(elem_list)
        print(x)
        d = elem_list[70:x-1:]
        print ('a ',a)
        print ('b ',b)
        print ('c ',c)
        print ('d ',d)
        key = []
        val = []
        key.append(a)                               # заполнение ключа в виде списка
        key.append(c)
        key = tuple(key)
        #print(key)
        val.append(b)  # заполнение значения в виде списка
        val.append(d)
        val = tuple(val)
        #print(val)
        out_dic[key] = val
    """
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
    """
    #print()
    #print('RETURN TO THE MAIN PROGRAMM')
    return out_dic
def parse_cdp_neighbors_sw(str_info,name):
    temp_in_func_info = {}
    #print('IN FUNCTION')
    #print()
    # print ()
    str_info = str_info[1:-1:]                          # отрезаем начальные и конечные символы строки
    # print ('str_info ', type(str_info))
    temp_in_func_info = str_info.split(",")             # перегоняем строку в список
    # print ('temp_in_func_info',type(temp_in_func_info),temp_in_func_info)
    del temp_in_func_info[0:12:]                        # срезаем лишние элементы
    # print (temp_in_func_info)
    out_dic = {}

    for elem_list in temp_in_func_info:
        # 'R1           Eth 0/1         122           R S I           2811       Eth 0/0'
        a = name
        print ('NAME',a)
        b = elem_list[2:4:]
        c = elem_list[15:22:]
        x = len(elem_list)
        d = elem_list[72:x:]
        key = []
        val = []
        key.append(a)                               # заполнение ключа в виде списка
        key.append(c)
        key = tuple(key)
        #print(key)
        val.append(b)  # заполнение значения в виде списка
        val.append(d)
        val = tuple(val)
        #print(val)
        out_dic[key] = val
    """
    {('R4', 'Fa0/1'): ('R5', 'Fa0/1'),
     ('R4', 'Fa0/2'): ('R6', 'Fa0/0')}
    """
    #print()
    #print('RETURN TO THE MAIN PROGRAMM')
    return out_dic

################### MAIN ####################
total_dic_r1 = {}
total_dic_r2 = {}
total_dic_r3 = {}
total_dic_sw1 = {}
total_dic = {}
r1 = (read_file('/home/ubuntu/workspace/python/tasks/8_module/8_2_b/sh_cdp_n_r1.txt'))
r2 = (read_file('/home/ubuntu/workspace/python/tasks/8_module/8_2_b/sh_cdp_n_r2.txt'))
r3 = (read_file('/home/ubuntu/workspace/python/tasks/8_module/8_2_b/sh_cdp_n_r3.txt'))
sw1 = (read_file('/home/ubuntu/workspace/python/tasks/8_module/8_2_a/sw1_sh_cdp_neighbors.txt'))

#r1 = (read_file('/home/const/PycharmProjects/8_task_1/sh_cdp_n_r1.txt'))
#r2 = (read_file('/home/const/PycharmProjects/8_task_1/sh_cdp_n_r2.txt'))
#r3 = (read_file('/home/const/PycharmProjects/8_task_1/sh_cdp_n_r3.txt'))
#sw1 = (read_file('/home/const/PycharmProjects/8_task_1/sw1_sh_cdp_neighbors.txt'))
print('READING FILE IS COMPLETE')

str_info_r1 = convert_info(r1)
str_info_r2 = convert_info(r2)
str_info_r3 = convert_info(r3)
str_info_sw1 = convert_info(sw1)

#print(str_info_r2)
print('CONVERT INFO IS COMPLETE')
print()

total_dic_r1 = parse_cdp_neighbors_r(str_info_r1, str_info_r1[2:4:])
total_dic_r2 = parse_cdp_neighbors_r(str_info_r2, str_info_r1[2:4:])
total_dic_r3 = parse_cdp_neighbors_r(str_info_r3, str_info_r1[2:4:])
total_dic_sw1 = parse_cdp_neighbors_sw(str_info_sw1,str_info_sw1[2:5:])
#print(total_dic_r1)
#print(total_dic_r2)
#print(total_dic_r3)
#print(total_dic_sw1)

#total_dic

total_dic.update(total_dic_r1) 
total_dic.update(total_dic_r2) 
total_dic.update(total_dic_r3) 
total_dic.update(total_dic_sw1) 
print('parse_cdp_neighbors is COMLETE')
print()
print(total_dic)
print ('DRAWING TOPOLOGY')
#draw_network_graph.draw_topology(total_dic)     

