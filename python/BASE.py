#!/usr/bin/env python

##### IMPORT

from time import sleep
# Регулярные выражения
import re
import os
# https://github.com/j1nn33/study/blob/master/python/devops/jupiter/man_6_OS.ipynb
import sys
import datetime
import csv


##### DEF
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
#### Работа с файлами [TO DO]

		
##### MAIN
if __name__ == '__main__':



###########################################################
#### CONSPECT


# RUN_BASH
###  output = run_bash("ls -la /etc/")
###  print(output['stdout'])
###  print(output['stderr'])
###  result = run_bash(f"ls -la /etc")
###  print (result)
###  #print(type(result))
###  #print (result.keys())
###  print ('OUT         ', result['stdout'])
###  print ('ERROR       ', result['stderr'])
###  print ('RETURN_CODE ', result['returncode'])

###  print(datetime.datetime.now().time())

###  temp_list_from_file = read_file ('/home/'+device)



# IF_THEN
###  if i == 45:
###      print('i is 45')
###  elif i == 35:
###      print('i is 35')
###  	
###  	
###  cat = 'spot'
###  if 's' in cat:
###      print("Found an 's' in a cat")
###      if cat == 'Sheba':
###          print("I found Sheba")
###      else:
###          print("Some other cat")
###  else:
###      print(" a cat without 's'")
###  
	
# FOR 

###  for i in range(10):
###      x = i*2
###      print(x)
###  
	
	
# WHILE

###  count = 0
###  while count < 3:
###      print(f"The count is {count}")
###      count += 1

# EXEPTION

###  try: 
###      #исполняемый код
###      pass
###  except Exeption as e:
###      #обработка исключения
###      pass
###  else:
###      #код, который будет исполнен в случае, когда нет исключения
###      pass
###  finally:
###      #код, который гарантированно будет исполнен последним (всегда исполняется)	
###  	pass
###  
###  # ----
###  
###  try:
###      result = 10 / 0
###  except ZeroDivisionError:
###      print("Деление на ноль!")
### 