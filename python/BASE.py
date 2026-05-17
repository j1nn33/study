#!/usr/bin/env python

##### IMPORT

from time import sleep
# Регулярные выражения
import re
import os, subprocess, sys, logging
# https://github.com/j1nn33/study/blob/master/python/devops/jupiter/man_6_OS.ipynb
import datetime
import csv, json, yaml



##### DEF

##### LINUX cmd RUN
def run_bash(cmd):
    """Простая функция для выполнения bash команды"""
    try:
        result = subprocess.run(
                cmd,
                shell=True,                # shell=True позволяет использовать пайпы (|), переменные окружения ($VAR) и wildcards (*)
                capture_output=True,
                #stdout=subprocess.PIPE,
                #sdterr=subprocess.PIPE,
                universal_newlines=True,     # Делает вывод output строковым не байтовым
                text=True
                )
        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        print(f" COMMAND FAILED" )
        return {'stdout': '', 'stderr': str(e), 'returncode': -1}

# ----------------------------------------------------------------------  
##### WORK EITH FILE 
##### READ FILE 


#### Процедура чтения из файла
def read_file (file_name):
    """читает файлы и передает результат в виде списка"""
    # print ("def read_file - print file name ", file_name)
    temp_list=[] 
    

    try:                                          # обработка исключения на наличие файла
        with open(file_name, 'r') as f:
            for line in f:
               temp_list.append(line.rstrip())    # исключиние дополнитеьлного символа перевода строки и заполнение вспомогательного списка
    except IOError:
        print('No such file in function ead_file')
    
    #print ("def read_file - print result ", temp_list)
    return temp_list


#### Процедура записи в файл  

def write_file(final_list, file_name):
     
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


# ----------------------------------------------------------------------  
##### LOGGING

def logging_in_func (n):
    total = 1
    logging.info  ('def LOGGING Start logging in functoin the argument is %s' %(n))
    logging.debug ('def LOGGING  Output DEBUG message from function var in func is' + str(total))
    logging.info  ('def LOGGING end logging in functoin')
    return 

# ----------------------------------------------------------------------  
# ----------------------------------------------------------------------  
# ----------------------------------------------------------------------  
# ----------------------------------------------------------------------  
# ----------------------------------------------------------------------  

		
##### MAIN
if __name__ == '__main__':



###########################################################
####                    CONSPECT
####                    TYPE 
    print ("")
    print ("#### PRINT TYPE START ####")
    print ("")
    # ----------------------------------------------------------------------   
    
      
    MY_TYPE_LIST = [1, 2, 3]
    print ('TYPE PRINT LIST ', MY_TYPE_LIST)
    print('TYPE PRINT LIST GET 1-st ELEMENT ', MY_TYPE_LIST[0])
    
    MY_TYPE_DICTIONARY = {'a': 1, 'b': 2, 'c': 3}
    print ('TYPE PRINT DICTIONARY',  MY_TYPE_DICTIONARY)
    print ('TYPE PRINT DICTIONARY ELRMENT',  MY_TYPE_DICTIONARY['b'])
    print ('TYPE PRINT DICTIONARY KEYS',  MY_TYPE_DICTIONARY.keys())
    print ('TYPE PRINT DICTIONARY VALUE',  MY_TYPE_DICTIONARY.values())
    print ('TYPE PRINT DICTIONARY KEY&VALUE',  MY_TYPE_DICTIONARY.items())
    # TUPLE
    
    # ----------------------------------------------------------------------
    print ("")
    print ("#### PRINT TYPE END ####")
    print ("----------------------------------------------------------------------")

####                   USEFULL FUNCTION
    print ("")
    print ("#### PRINT USEFULL FUNCTION START ####")
    print ("")
    # ----------------------------------------------------------------------
    
    print("USEFULL FUNCTION - TIME ", datetime.datetime.now().time())
    
    # Получить путь исполняемого файла 
    absolute_path = os.path.abspath(__file__)
    print(f"USEFULL FUNCTION Абсолютный путь к исполняему файлу: {absolute_path}")
    
    # Получаем директорию, содержащую текущий файл
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"USEFULL FUNCTION BASE_DIR: {base_dir}")

    #                   OS
    # https://github.com/j1nn33/study/blob/master/python/devops/jupiter/man_6_OS.ipynb
    # Получаем текущий рабочий каталог
    current_dir = os.getcwd()
    print ('USEFULL FUNCTION - CURRENT DIR ', current_dir )
    # /home/tooks/repo
    
    # os.path.split отделяет конечный уровень пути от родительского пути
    print (os.path.split(current_dir))
    # ('/home/tooks', 'repo')
    
    # os.path.basename возвращает название конечного каталога
    os.path.basename(current_dir)
    # 'repo'
    
    # обход дерева каталогов
    while os.path.basename(current_dir):
        current_dir=os.path.dirname(current_dir)
        print(current_dir)
    
    # Меняем текущий рабочий каталог.
    # os.chdir('/tmp')
    
    # В os.environ хранятся переменные среды, значения которых были 
    # установлены при загрузке модуля
    # os.environ.get('LOGLEVEL')
    # os.environ['LOGLEVEL'] = 'DEBUG'
    # os.environ.get('LOGLEVEL')

    # ----------------------------------------------------------------------
    print ("")
    print ("#### PRINT USEFULL FUNCTION END ####")
    print ("----------------------------------------------------------------------")
####                   FUNCTION 
    print ("")
    print ("#### FUNCTION START####") 
    print ("")  
    # ----------------------------------------------------------------------
      
    #                 RUN_BASH
    print ("#### FUNCTION RUN_BASH START ####")
    print ("")
    output = run_bash('ls -la /etc/')
    # print(output['stdout'])
    # print(output['stderr'])
    result = run_bash(f"ls -la /etc")
    #print (result)
    #print(type(result))
    #print (result.keys())
    #print ('OUT         ', result['stdout'])
    #print ('ERROR       ', result['stderr'])
    #print ('RETURN_CODE ', result['returncode'])
    print ("")
    print ("#### FUNCTION RUN_BASH END ####")
    print ("----------------------------------------------------------------------") 

    # -----------------------------------------------------------------
    #                WORK WITH FILE
    print ("")
    print ("#### WORK WITH FILE START ####")
    print ("")
    ##### Примеры для разных форматов файлов TXT, JSON, CSV, YML, XML  
    ##### https://github.com/j1nn33/study/blob/master/python/devops/jupiter/man_3_file.ipynb
    ##### https://github.com/j1nn33/study/tree/master/python/conspect/FILE_%26_tempates
    
    
          
    # Получаем директорию, содержащую текущий исполняемого файла, в этой же директории лежит файл для чтения 
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"WORK WITH FILE BASE_DIR: {base_dir}")
    input_file_path = os.path.join(base_dir, 'TEST_FILE_SOURCE.txt')
    print ("WORK WITH FILE INPUT FILE: ", input_file_path)
    output_file_path = os.path.join(base_dir, 'TEST_FILE_OUTPUT.txt')
    print ("WORK WITH FILE OUTPUT FILE: ", output_file_path)
   
    data_source = read_file (input_file_path) 
    print ("WORK WITH FILE print " ,data_source)
    # Запись идет добавлением информации в файл 
    # добавление отделяется '---------------------------------------------'
    # write_file(data_source, output_file_path)
    
    print ("")
    print ("#### WORK WITH FILE STOP ####") 
    print ("----------------------------------------------------------------------") 
    # ----------------------------------------------------------------------
    #              LOGGING
    print ("")
    print ("#### WORK LOGGING START ####")
    print ("")
    BASE_FORMAT_LOG = " [%(levelname)-6s] %(message)s"
    FILE_FORMAT_LOG = "[%(asctime)s]" + BASE_FORMAT_LOG
    logging.basicConfig(level=logging.DEBUG,  format= FILE_FORMAT_LOG)
    logging.info('LOGGING Start of program')
    logging_in_func(3)
    logging.info ('LOGGING End of program')
    print ("")
    print ("#### WORK LOGGING STOP ####")
    print ("")
    # ----------------------------------------------------------------------
    #print ("")
    #print ("#### WORK ---- START ####")
    #print ("")
    
    #print ("")
    #print ("#### WORK ---- STOP ####")
    #print ("")
    # ----------------------------------------------------------------------
    #print ("")
    #print ("#### WORK ---- START ####")
    #print ("")
    
    #print ("")
    #print ("#### WORK ---- STOP ####")
    #print ("")
    # ----------------------------------------------------------------------
    #print ("")
    #print ("#### WORK ---- START ####")
    #print ("")
    
    #print ("")
    #print ("#### WORK ---- STOP ####")
    #print ("")
    # ----------------------------------------------------------------------
    #print ("")
    #print ("#### WORK ---- START ####")
    #print ("")
    
    #print ("")
    #print ("#### WORK ---- STOP ####")
    #print ("")
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
####                 BASE CONSTRUCTION

    print ("#### BASE CONSTRUCTION START ####")
    print ("")
    # ----------------------------------------------------------------------
#                 IF_THEN

    i = 35
    if i == 45:
        print('BASE CONSTRUCTION IF_THEN i is 45')
    elif i == 35:
        print('BASE CONSTRUCTION IF_THEN i is 35')
    	
    # ----
  
    cat = 'spot'
    if 's' in cat:
        print("BASE CONSTRUCTION IF_THEN Found an 's' in a cat")
        if cat == 'Sheba':
            print("BASE CONSTRUCTION IF_THEN I found Sheba")
        else:
            print("BASE CONSTRUCTION IF_THEN Some other cat")
    else:
        print("BASE CONSTRUCTION IF_THEN a cat without 's'")
    

	# ----------------------------------------------------------------------
#                FOR 

    for i in range(3):
        x = i*2
        print("BASE CONSTRUCTION FOR ", x)
    
	
	# ----------------------------------------------------------------------
#              WHILE

    count = 0
    while count < 3:
        print(f"BASE CONSTRUCTION WHILE the count is {count}")
        count += 1
    
    # ----------------------------------------------------------------------
    print ("")
    print ("#### BASE CONSTRUCTION END ####")
    print ("----------------------------------------------------------------------")
#             EXEPTION

    try: 
        #исполняемый код
        pass
    except Exeption as e:
        #обработка исключения
        pass
    else:
        #код, который будет исполнен в случае, когда нет исключения
        pass
    finally:
        #код, который гарантированно будет исполнен последним (всегда исполняется)	
    	pass
 
# ----------------------------------------------------------------------
    
#    try:
#        result = 10 / 0
#    except ZeroDivisionError:
#        print("Деление на ноль!")
   