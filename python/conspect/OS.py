#!/usr/bin/env python
"""
import os

os.chdir("/tmp")

s = os.getcwd()
print ( 'имя текущего рабочего каталога ', s )

#s = os.mkdir("/tmp/os_mod_explore")
print ( 'создали новый каталог '  )

s = os.listdir("/tmp/os_mod_explore")
print ( 'содержимое каталога ', s )

s = os.stat('/tmp/os_mod_explore')
print ( "вывод статистики по новому каталогу", s)

# os.rename("/tmp/os_mod_explore/terert", "/tmp/os_mod_explore/terert_renamed")
print ('переименование ')

os.rmdir("/tmp/os_mod_explore/terert_renamed")
os.rmdir("/tmp/os_mod_explore/")

print ('удаление каталога ')
"""

#!/usr/bin/env python
# Сценарий обхода каталога

import os


path = "/boot"

def enumeratepaths(path=path):
    """Возвращает пути ко всем файлам в каталоге в виде списка"""
    path_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        for file in filenames:
            fullpath = os.path.join(dirpath, file)
            path_collection.append(fullpath)

    #print (path_collection)
    return path_collection
#############################################

def enumeratefiles(path=path):
    """Возвращает имена всех файлов в каталоге в виде списка"""
    file_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        print ('filenames ',filenames)
        for file in filenames:
            file_collection.append(file)
            print(file)

    #print (file_collection)
    return file_collection
#############################################

def enumeratedir(path=path):
    """Возвращает имена всех подкаталогов в каталоге в виде списка"""
    dir_collection = []
    for dirpath, dirnames, filenames in os.walk(path):
        for dir in dirnames:
            dir_collection.append(dir)

    return dir_collection
#############################################

if __name__ == "__main__":

    print (" Recursive listing of all paths in a dir: ")
    for path in enumeratepaths(path):
        pass
        #print (path)

    print (enumeratefiles())


    print (" Recursive listing of all files in dir: ")
    for file in enumeratefiles():
        print (file)

    print (enumeratefiles())


    print (" Recursive listing of all dirs in dir: ")
    for dir in enumeratedir(path):
        print (dir)


    print (enumeratedir())

