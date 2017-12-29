# Upgrade задании 7.4. на примере файла config_r1.txt
# В нем есть разделы с большей вложенностью, например, разделы: interface Ethernet0/3.100
# функция config_to_dict должна обрабатывать следующий уровень вложенности.
# (При этом, не привязываясь к конкретным разделам. Она должна быть универсальной, и сработать, если это будут другие разделы.)
# Если уровня вложенности два:
#     то команды верхнего уровня будут ключами словаря, а команды подуровней - списками
# Если уровня вложенности три:
#     самый вложенный уровень должен быть списком, а остальные - словарями.

"""Логика работы
+ 1 исходные данные (список ignore)
+ 2 функция ignore_command возвращает True или False
+ 3 функция generator_dict 
3 функция config_to_dict 
    + принимает файл  (проводит проверку на существование и преобразует его в список temp_list)
    + обрабока строк списка temp_list
        + вызов функции ignore
        + проверка строк списка temp_list на удаление по результатам работы ignore.  
        + заполнение промежуточного списка с удаленными элементами    
    + формирование промежуточных списков для функции generator_dict 
    + выполнение функции generator_dict и заполнения словаря key = level_1 items = level_2
    + выполнение функции generator_dict и заполнения словаря key = level_2 items = level_3   
    - формирование итогового словаря
    - вывод словаря 
+ 4 вызов основной функции
"""
###################################################

ignore = ['duplex', 'alias', 'Current configuration']

###################################################

def ignore_command(command, ignore):             
    """
    Функция проверяет содержится ли в команде слово из списка ignore.
    command - строка. Команда, которую надо проверить
    ignore - список. Список слов
    any - Возвращает True, если в команде содержится слово из списка ignore, False - если нет
    """
    return any(word in command for word in ignore)

###################################################

def generator_dict (input_list):
    """
    функция генерируте словарь на основе переданного ей списка
    1. проход по input_list - создать список command_level_1 
    2. если command == (' ') те не команда первого уровня то 
           - заполняем список 
       иначе
           - заполняем список  command_level_2 для команды первого уровня 
           - заносим значение key в словарь и список в качестве значения
           - запоминаем в key command отчищам список 
    """
    command_level_1 = dict()                     # глобальные команды или верхнего уровня (словарь)
    command_level_1_list =[]
    command_level_2 = []                         # подкоманды команды (список)
    for command in input_list:              # избавляемся от первых 2-х и последней строки в начале файла 
        if not command.startswith(' '):
            command_level_1_list.append (command)
            #command_level_1[command] = command_level_2
        else:
            pass
    #print ('command_level_1_list', command_level_1_list)
    j=0                                          # счетчик для элементов из command_level_1_list
    for command in input_list:              # избавляемся от первых 2-х и последней строки в начале файла 
        if command.startswith(' '):
            #print ('command -2 ' ,command)
            command_level_2.append(command[1::])
            #print (command_level_2)
        else:
            #print ('command_level_2          ',command_level_2)
            #print ('command_level_1_list[j]  ', command_level_1_list[j])
            command_level_1[command_level_1_list[j-1]] = command_level_2
            command_level_2 = []
            if j<len(command_level_1_list):
                j=j+1
            else:
                pass
    #print ('итоговый cловарь в функции')
    #print (command_level_1)      
    return command_level_1

###################################################    

def config_to_dict (cfg_file):
    temp_list=[]                                   
    ############################################### открытие файла и обработка исключения на наличие файла
    try:                                           
        with open('/home/ubuntu/workspace'+cfg_file, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('No such file')
    #print('\n'.join(temp_list)) 
    ############################################## вызов функции ignore     
    temp_list_2=[]                             # промежуточный список     
    for command in temp_list:
        if  ignore_command(command, ignore) == True:
            continue
        elif command.startswith('!'):
            continue
        else:
            temp_list_2.append(command)
    #print('\n'.join(temp_list_2))            
    ##############################################
    temp_list_4=[]                            # промежуточный список для temp_list_3 для формированя словаря  command_level_1
    for command in temp_list_2:               # избавляемся от первых 2-х и последней строки в начале файла 
        if command.startswith('  '):
            continue
        else:
            temp_list_4.append(command)
    #print('\n'.join(temp_list_4)) 
    temp_list_3=[]                            # промежуточный список для temp_list_3 для формированя словаря  command_level_2
    for command in temp_list_2:               # избавляемся от первых 2-х и последней строки в начале файла 
        if not command.startswith(' '):
            continue
        else:
            temp_list_3.append(command[1::])
    #print('\n'.join(temp_list_3))              
    ##############################################
    #command_level_0 = generator_dict(temp_list_2)         # заполнения словаря key = level_1 items = level_2, items = level_3 
    command_level_1 = generator_dict(temp_list_4[2::])    # заполнения словаря key = level_1 items = level_2   
    #print (command_level_1)
    command_level_2 = generator_dict(temp_list_3)         # заполнения словаря key = level_2 items = level_3
    #print (command_level_2)
    
    ##############################################
    command_level_final = {}
    """
    Логика заполнения вложенного словаря
    1 пробегаем по всем ключам 1 словаря 
        создаем временный словарь - (будет использоваться в качестве значений итогового)
        в цикле пробегаемся по ключам 2 словаря (ключи и значения которого будут вложенны)
            если ключи второго словаря присутсуют в списке занчений первого словаря то 
                 заполняем временный словарь
                 выходим из цикла
            заполняем итоговый словарь 
    """
    for key_1 in command_level_1:
        #print('key_1 ',key_1)
        #print ('item-1', command_level_1[key_1]) 
        dict_temp={}                               # временный словарь для значениий итогового словаря 
        for key_2 in command_level_2:
            #print('key_2',key_2)
            #print ('item-1', command_level_1[key_1])
            if key_2 in command_level_1[key_1]:
                #print (key_2, command_level_2[key_2])
                #print (command_level_2[key_2])
                dict_temp[key_2]=command_level_2[key_2]
            
            command_level_final[key_1]=dict_temp
            
    print (command_level_final)      
    return

##################################################

config_to_dict ('/python/tasks/7 _function/config_r1.txt')

"""
{'interface Ethernet0/3.100':{'encapsulation dot1Q 100':[],
                              'xconnect 10.2.2.2 12100 encapsulation mpls':['backup peer 10.4.4.4 14100','backup delay 1 1']}}

"""                            