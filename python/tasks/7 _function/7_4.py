#       Создать функцию, которая обрабатывает конфигурационный файл коммутатора и возвращает словарь:
#            Все команды верхнего уровня (глобального режима конфигурации), будут ключами.
#                Если у команды верхнего уровня есть подкоманды, они должны быть в значении у
#                    соответствующего ключа, в виде списка (пробелы вначале можно оставлять).
#                Если у команды верхнего уровня нет подкоманд, то значение будет пустым списком
#            Функция ожидает в качестве аргумента имя конфигурационного файла. config_sw1.txt
#            При обработке конфигурационного файла, надо игнорировать строки, которые
#                начинаются с '!', а также строки в которых содержатся слова из списка ignore.
#                Для проверки надо ли игнорировать строку, использовать функцию ignore_command.

"""Логика работы
+ 1 исходные данные (список ignore)
+ 2 функция ignore_command возвращает True или False
3 функция config_to_dict 
    + принимает файл  (проводит проверку на существование и преобразует его в список temp_list)
    + обрабока строк списка temp_list
        + вызов функции ignore
        + проверка строк списка temp_list на удаление по результатам работы ignore.  
        + заполнение промежуточного списка с удаленными элементами    
        + алгоритм парсера
        + заполнение словаря
    + вывод словаря 
+ 4 вызов основной функции
"""

ignore = ['duplex', 'alias', 'Current configuration']
###################################################
def ignore_command(command, ignore):             # 1 var.
    """
    Функция проверяет содержится ли в команде слово из списка ignore.
    command - строка. Команда, которую надо проверить
    ignore - список. Список слов
    any - Возвращает True, если в команде содержится слово из списка ignore, False - если нет
    """
    return any(word in command for word in ignore)
"""
def ignore_command(command, ignore):             # 2 var/
    a=False
    for i in ignore:
        if command.find(i) !=-1:                  # поиск игнорируемого слова i  в строке x 
            a = True
        else:
            pass
    return a
"""
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
    temp_list_2=[]
    for command in temp_list:
        if  ignore_command(command, ignore) == True:
            continue
        elif command.startswith('!'):
            continue
        else:
            temp_list_2.append(command)
    #print('\n'.join(temp_list_2))
    ############################################## алгоритм парсера
    """логика парсера
    1. проход по temp_list_2 - создать список command_level_1 
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
    for command in temp_list_2[2::]:             # избавляемся от первых 2-х и последней строки в начале файла 
        if not command.startswith(' '):
            command_level_1_list.append (command)
            #command_level_1[command] = command_level_2
        else:
            pass
    #print ('command_level_1_list', command_level_1_list)
    j=-1                                          # счетчик для элементов из command_level_1_list
    for command in temp_list_2[2::]:           # избавляемся от первых 2-х и последней строки в начале файла 
        if command.startswith(' '):
            #print ('command -2 ' ,command)
            command_level_2.append(command)
            #print (command_level_2)
        else:
            #print ('command_level_2          ',command_level_2)
            print ('command_level_1_list[j]  ', command_level_1_list[j])
            command_level_1[command_level_1_list[j]] = command_level_2
            command_level_2 = []
            if j<len(command_level_1_list):
                j=j+1
            else:
                pass
            
        
    #############################################ВЫВОД
    print ('итоговый cловарь')
    print (command_level_1)                                        
    return
##################################################
config_to_dict ('/python/tasks/7 _function/config_sw1.txt')