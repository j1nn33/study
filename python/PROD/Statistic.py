#!/bin/python3
#----------------------------
# Program  by Konstantin. B.
#
# Version	Date		
# 1.0 		2018
# Info
#----------------------------
# скрипт сбора статистики с компьютера

import subprocess



def uname_func():   # вывод информации о ядре 
    uname = "uname"
    uname_arg = "-a"
    print ("Gathering system information with %s command: ")
    subprocess.call([uname, uname_arg])
def disk_func():    # вывод об использовании дискового простиранства
    diskspace = "df"
    diskspace_arg = "-h"
    print ("Gathering diskspace information %s command: ")
    subprocess.call([diskspace, diskspace_arg])

if __name__ == '__main__':
    print ('==========================')
    print ()
    uname_func()
    print ()
    print ('==========================')
    print ()
    disk_func()

