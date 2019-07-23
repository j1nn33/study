# -*- coding: utf-8 -*-
# python3 ./python/PROD/dgate/generate.py
"""
СКРИПТ ГЕНЕРАЦИИ ФАЙЛА dgate.conf

- чтение исходных данный из файла input.txt
- заполнение результатом выходного файла

ИСХОДНЫЕ ДАННЫЕ 
Свой объект = МТС=БСПС:ЮПИТЕР  
 УG01:YG01  

 Удаленные объекты= МТС=БСПС:ЮПИТЕР
 МZ00:MZ$$, УG02:YG02

 роли в БСПС 
 ГМ, ОБИ 1

------------------------------------------------------------------------------
 upmts:MZ$$:МZ00::0:3<>bsps:pГМ@МZ00:::0:3 #Почта получателя в Юпитере
 upmts:MZ$$:МZ00::0:3<>bsps:pОБИ 1@МZ00:::0:3 #Почта получателя в Юпитере
 upmts:YG02:УG02::0:3<>bsps:pГМ@УG02:::0:3 #Почта получателя в Юпитере
 upmts:YG02:УG02::0:3<>bsps:pОБИ 1@УG02:::0:3 #Почта получателя в Юпитере
 bsps:pГМ@УG01:::0:3<>upmts:YG01:::0:3   #Почта отправителя якобы от Юпитера
 bsps:pОБИ 1@УG01:::0:3<>upmts:YG01:::0:3   #Почта отправителя якобы от Юпитера
 1:p*@МZ00::0:3>2:МZ00::
 1:p*@УG02::0:3>2:УG02::

------------------------------------------------------------------------------
ЕСЛИ ИМЯ ОБЪЕКТА НЕ СОВПДАЕТ С ИМЕНЕМ БСПС, 
то в результате необходимо ввести корректировки  

МТС    БСПС(юпитер)    БСПС(бспс)
И100   Юпитер И1       БСПС И1

upmts:И1$$:И100::0:3<>bsps:pГЛ@Юпитер И1:::0:3 #Почта получателя в Юпитере

1:p*@БСПС И1::0:3>2:И100:

"""

#======================================  

#def generate_config(name_object, name_upiter, name_bsps, role):
def generate_config(local_object, remote_object, role):
    """
    Функция 
    генерации строчек конфигурационного файла dgate.conf
    """
    generate_list=[]
    
    print ('--------------------------')
    print ('|      Исходные данные   |')
    print ('--------------------------')
    print (' Локальный объект МТС (ru00), Юпитер (en$$)  __', local_object)
    print (' Удаленные объекты МТС (ru00), Юпитер (en$$) __', remote_object)
    print (' Роли _________________________________________', role)
    print ('--------------------------')
    print ('|       Результат        |')
    print ('--------------------------')
    
    for item_remote in remote_object:
        for item_role in role: 
            st = 'upmts:{1}:{0}::0:3<>bsps:p{2}@{0}:::0:3 #Почта получателя в Юпитере'.format(item_remote, remote_object[item_remote], item_role)
            print (st)
            generate_list.append (st)
    
    for item_local in local_object:
        for item_role in role:
            st = 'bsps:p{2}@{0}:::0:3<>upmts:{1}:::0:3   #Почта отправителя якобы от Юпитера'.format(item_local, local_object[item_local], item_role)
            print (st)
            generate_list.append (st)
            
    for item_remote in remote_object:
        st = '1:p*@{0}::0:3>2:{0}::'.format(item_remote)
        print (st)
        generate_list.append (st) 
        
    #print (generate_list)
    return generate_list 




#======================================  

def test_1 (generate_config):
    """
    функция тестирования test_1
    """ 
    print (test_1.__doc__)
    
    # исходные данные 
   
    local_object = {'УG01':'YG01'}
    remote_object= {'МZ00':'MZ$$','УG02':'YG02'}
    role =  ['ГМ']
    
    
    # контрольные значения 
   
    control_list = ['upmts:MZ$$:МZ00::0:3<>bsps:pГМ@МZ00:::0:3 #Почта получателя в Юпитере',
                    'upmts:YG02:УG02::0:3<>bsps:pГМ@УG02:::0:3 #Почта получателя в Юпитере', 
                    'bsps:pГМ@УG01:::0:3<>upmts:YG01:::0:3   #Почта отправителя якобы от Юпитера',
                    '1:p*@МZ00::0:3>2:МZ00::',
                    '1:p*@УG02::0:3>2:УG02::',
                    ]
    
    # Алгоритм тестирования
   
    generate_list = generate_config(local_object, remote_object, role)
    
    if  (generate_list[0] == control_list[0]) and (generate_list[1] == control_list[1]):
        print ('')
        print ('upmts  - OK')
    else:
        print ('')
        print ('upmts - FAIL')
        print ('')
        print('полученое   значение -', generate_list[0])
        print('контрольное значение -', control_list[0])
        print('полученое   значение -', generate_list[1])
        print('контрольное значение -', control_list[1])
        
    if generate_list[2] == control_list[2]:
        print ('')
        print ('bsps   - OK')
    else:
        print ('')
        print ('bsps - FAIL')
        print ('')
        print('полученое   значение -', generate_list[2])
        print('контрольное значение -', control_list[2])
        
    
    if (generate_list[3] == control_list[3]) and (generate_list[4] == control_list[4]):
        print ('')
        print ('tunnel - OK')
    else:
        print ('')
        print ('tunnel - FAIL')
        print ('')
        print('полученое   значение -', generate_list[3])
        print('контрольное значение -', control_list[3])
        print('полученое   значение -', generate_list[4])
        print('контрольное значение -', control_list[4])
    
#======================================        

def read_from_file():
    """
    функция открытия файла и передача его содержимого в список
    ./input.txt
    """
    temp_list=[]                                # инициализация вспомогательного списка  
    # открытие файла
    try:                                          # обработка исключения на наличие файла
       with open('./input.txt', 'r') as f:
           for line in f:
               temp_list.append(line.rstrip())  # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
       print('No such file')


    #print(temp_list)
    return temp_list
#======================================  

def processing_data():
    """
    функция обработки содержимого файла:
    удаляет коментарии и конвертирует содержимое к необходимым данным
    """
    final_list = []
    local_object_list = []
    remote_object_list = []
    local_object = {}
    remote_object = {}
    role = []
    temp_list=read_from_file()                # открытие файла с исходными данными
                                              # удаление служебной информации
    for x in temp_list:
        if x[0] !='#': final_list.append(x)
    #print (final_list)
    #print (type(final_list[0]), final_list[0])
    #print (final_list[1])
    #print (final_list[2])
    
    # преобразование данных для локального объекта
    local_object_list = final_list[0].split(', ')
    #print ('local_object_list', type(local_object_list), local_object_list)
    for x in local_object_list:
        temp_item_list = []
        temp_item_list = x.split(':')
        #print (temp_item_list)
        local_object.update({temp_item_list[0]:temp_item_list[1]})
        
    # преобразование данных для удаленных объектов
    remote_object_list = final_list[1].split(', ')
    #print ('remote_object_list', type(remote_object_list), remote_object_list)
    for x in remote_object_list:
        temp_item_list = []
        temp_item_list = x.split(':')
        #print (temp_item_list)
        remote_object.update({temp_item_list[0]:temp_item_list[1]})
        
    # преобразоване данных для ролей
    role = final_list[2].split(', ')
    
    #print ('\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\')
    #print ('local_object ',type(local_object), local_object)
    #print ('remote_object',type(remote_object), remote_object)
    #print ('role         ',type(role), role)
    #generate_config (local_object, remote_object, role)
    return local_object, remote_object, role

#======================================     

def create_result_file(final_list):
     # имя выходного файла out.txt
     file_name="./out.txt" 

     # определяем для открытого файла переменую f
     # и выполняет набор инструкций. После их выполнения файл автоматически закрывается. 
     # Даже если при выполнении инструкций в блоке with возникнут какие-либо исключения,
     # то файл все равно закрывается.
     temp_list = final_list
     with open(file_name, 'a') as f:        # определяем для открытого файла переменую f
         line = '---------------------------------------------'
         f.write(line+'\n') 
         for line in temp_list:
             #print (line)
             #f.write(str(line)) 
             f.write(str(line)+'\n') 
             #f.write(line+'\n')             # +'\n' для переноса строк
     f.close()


   
#======================================   

if __name__ == "__main__":
    
   # Модуль контрольного тестирования
   #
   #test_1 (generate_config)         # test1 тестирование generate_config
   #
   ##################################
   # 
   # Загрузка данных из файла и обработка
   #
   local_object = {}
   remote_object = {}
   role = []
   local_object, remote_object, role = processing_data()
   
   #print ('DATA after processing_data')
   #print (local_object)
   #print (remote_object)
   #print (role)
   # 
   #generate_config(local_object, remote_object, role)
   final_list = []
   final_list = generate_config(local_object, remote_object, role)
   #
   # запись результатов в выходной файл
   #
   create_result_file(final_list) 