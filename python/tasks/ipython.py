"""
import os
import re
dict_device={}

line_in_file= ('SW1              Eth 0/0            125          S I      WS-C3750- Eth 0/2')
match =re.search('(?P<my_int>\S+)\s+(?P<neighbors_name>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',line_in_file) 
# получение последнего знаячения этой строки
#posit_end=re.search('(?P<my_int>\S+)\s+(?P<neighbors_name>\S+\s\S+).+?(?P<neighbors_int>[Eth]\S+\s\d+\S\d+)',out_file_string).end()
my_int = match.group('my_int')
neighbors_name =match.group('neighbors_name')
neighbors_int =match.group('neighbors_int') 
dict_temp2= {}
dict_temp1= {}
dict_temp1[neighbors_name]= neighbors_int   
dict_temp2[my_int]=dict_temp1
#print (dict_temp2)
#out_file_string = out_file_string[posit_end::]           # срезаем общую строку на строку конфига из файла
dict_device.update(dict_temp2)
print(dict_device)
"""

def a():
    x=1
    y=2
    return x,y
    
q,w=a()
print (q , w)